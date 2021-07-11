import numpy as np
import pandas as pd
import torch
import math
from simplification.cutil import simplify_coords

def resample(x, y, spacing=1.0):
    output = []
    n = len(x)
    px = x[0]
    py = y[0]
    cumlen = 0
    pcumlen = 0
    offset = 0
    for i in range(1, n):
        cx = x[i]
        cy = y[i]
        dx = cx - px
        dy = cy - py
        curlen = math.sqrt(dx*dx + dy*dy)
        cumlen += curlen
        while offset < cumlen:
            t = (offset - pcumlen) / curlen
            invt = 1 - t
            tx = px * invt + cx * t
            ty = py * invt + cy * t
            output.append((tx, ty))
            offset += spacing
        pcumlen = cumlen
        px = cx
        py = cy
    output.append((x[-1], y[-1]))
    return output


def normalize_resample_simplify(strokes, epsilon=1.0, resample_spacing=1.0):
    if len(strokes) == 0:
        raise ValueError('empty image')

    # find min and max
    amin = None
    amax = None
    for x, y in strokes:
        cur_min = [np.min(x), np.min(y)]
        cur_max = [np.max(x), np.max(y)]
        amin = cur_min if amin is None else np.min([amin, cur_min], axis=0)
        amax = cur_max if amax is None else np.max([amax, cur_max], axis=0)

    # drop any drawings that are linear along one axis
    arange = np.array(amax) - np.array(amin)
    if np.min(arange) == 0:
        raise ValueError('bad range of values')

    arange = np.max(arange)
    output = []
    for x, y in strokes:
        xy = np.array([x, y], dtype=float).T
        xy -= amin
        xy *= 255.
        xy /= arange
        resampled = resample(xy[:, 0], xy[:, 1], resample_spacing)
        simplified = simplify_coords(resampled, epsilon)
        xy = np.around(simplified).astype(np.uint8)
        output.append(xy.T.tolist())

    return output


def resample_to(drawing, n):
    drawing = [s for s in drawing if s.shape[1] > 1]
    drawing = [s.astype(np.float) for s in drawing]

    segment_lengths = [np.linalg.norm(np.diff(s[:2], axis=1), axis=0) for s in drawing]
    stroke_lengths = [seg_len.sum() for seg_len in segment_lengths]
    cum_seg_len = [np.concatenate([np.array([0]), sl.cumsum()]) for sl in segment_lengths]
    length_per_point = np.clip(np.array(stroke_lengths).sum() / n, 0.25, 500)

    new_stroke_points = np.clip((stroke_lengths / length_per_point), 2, n).astype(np.int)
    j = len(new_stroke_points) - 1
    err = n - new_stroke_points.sum()
    while err != 0 and j >= 0:
        new_stroke_points[j] = max(new_stroke_points[j] + err, 2)
        err = n - new_stroke_points.sum()
        j += -1

    new_seg_samples = [np.linspace(0, sl, nsp) for sl, nsp in zip(stroke_lengths, new_stroke_points)]

    out = [np.array([
        np.interp(nss, csl, s[0]),
        np.interp(nss, csl, s[1]),
        np.interp(nss, csl, s[2])
    ]) for s, nss, csl in zip(drawing, new_seg_samples, cum_seg_len)]

    return out


def process_raw(drawing, out_size, actual_points, padding):
    drawing = resample_to(drawing, actual_points)

    points = np.zeros((3, out_size), dtype=np.uint8)
    indices = np.full(actual_points, padding, dtype=np.int64)

    cursor_points = 0
    cursor_indices = 0
    for s in drawing:
        remaining_space_points = out_size - cursor_points
        remaining_space_indices = actual_points - cursor_indices

        num_points = s.shape[1]

        padded_s = np.pad(s, [[0, 0], [padding, padding]], mode='edge')
        num_padded_points = padded_s.shape[1]
        keep_new = min(num_padded_points, remaining_space_points)
        new_cursor_points = cursor_points + keep_new
        points[:, cursor_points:new_cursor_points] = padded_s[:, :keep_new]

        indices_new_start = min(cursor_points + padding, out_size - padding)
        keep_new_indices = min(num_points, remaining_space_indices)
        indices_new_end = min(indices_new_start + keep_new_indices, out_size - padding)
        indices_new = np.arange(indices_new_start, indices_new_end, 1)
        num_indices_new = indices_new.shape[0]
        new_cursor_indices = cursor_indices + num_indices_new
        indices[cursor_indices:new_cursor_indices] = indices_new

        cursor_points = new_cursor_points
        cursor_indices = new_cursor_indices

    drawing_max = points.max(axis=1)
    drawing_min = points.min(axis=1)
    size = (drawing_max - drawing_min)
    largest_dimension = size[:2].max()
    xy_scale = 128 if (largest_dimension // 2) == 0 else largest_dimension // 2
    time_scale = 128 if size[2] == 0 else size[2]
    middle = drawing_min + size / 2
    points = (points - middle.reshape((3, 1))) / np.array([[xy_scale], [xy_scale], [time_scale]])

    return points, indices


def eval_single(drawing, out_size=512, actual_points=128, padding=16):
    data = [np.array(s) for s in drawing]
    maximums = np.stack([s.max(1) for s in data]).max(0)
    minimums = np.stack([s.min(1) for s in data]).min(0)
    spatial_scale = max(maximums[0]-minimums[0], maximums[1]-minimums[1])
    spatial_scale = spatial_scale if spatial_scale != 0 else 1
    time_scale = maximums[2] - minimums[2]
    time_scale = time_scale if time_scale != 0 else 1
    scale = np.array([spatial_scale, spatial_scale, time_scale])
    data = [(s - minimums[:, None])/scale[:, None] for s in data]
    data = [np.clip(s*255, 0, 255) for s in data]

    points, indices = process_raw(data, out_size, actual_points, padding)
    return torch.from_numpy(points.astype(np.float32)), torch.from_numpy(indices)
