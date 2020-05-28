import pandas as pd
import numpy as np
import math
from tqdm import tqdm
from tqdm._tqdm import trange
from simplification.cutil import simplify_coords
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--csv', type=str, default='test_cp.csv')
args = parser.parse_args()

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
    for x, y, _ in strokes:
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
    for x, y, _ in strokes:
        xy = np.array([x, y], dtype=float).T
        xy -= amin
        xy *= 255.
        xy /= arange
        resampled = resample(xy[:, 0], xy[:, 1], resample_spacing)
        simplified = simplify_coords(resampled, epsilon)
        xy = np.around(simplified).astype(np.uint8)
        output.append(xy.T.tolist())

    return output


if __name__ == '__main__':
    df = pd.read_csv("test_simplified/" + args.csv)
    for t in tqdm(range(len(df))):
        draw = eval(df['drawing'][t])
        draw = normalize_resample_simplify(draw)
        cnt = 0
        for i in range(len(draw)):
            t_list = []
            for j in range((len(draw[i][0]))):
                t_list.append(cnt)
                cnt += 1
            draw[i].append(t_list)
        df.loc[t, 'drawing'] = str(draw)
    
    df.to_csv(args.csv[:-4] + "_simplified.csv", index=False)
