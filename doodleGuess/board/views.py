from django.shortcuts import HttpResponse, render
import json
from utils.preprocess import normalize_resample_simplify
from utils.eval import test, test_person


# Create your views here.


def draw(request):
    return render(request, 'index.html')


def welcome(request):
    return render(request, 'main.html')


def process(request):
    if request.method == 'POST':
        data = json.loads(request.body, strict=False)
        drawing = []
        for i in range(len(data)):
            x_list = []
            y_list = []
            for pos in data[i]:
                x_list.append(pos['x'])
                y_list.append(pos['y'])
            drawing.append([x_list, y_list])
        drawing = normalize_resample_simplify(drawing)
        cnt = 0
        for i in range(len(drawing)):
            t_list = []
            for j in range((len(drawing[i][0]))):
                t_list.append(cnt)
                cnt += 1
            drawing[i].append(t_list)
        global pred
        pred = test(drawing)
        pred = json.dumps(pred)
        return HttpResponse(pred)
    return HttpResponse("OK")


def process_person(request):
    if request.method == 'POST':
        data = json.loads(request.body, strict=False)
        drawing = []
        for i in range(len(data)):
            x_list = []
            y_list = []
            for pos in data[i]:
                x_list.append(pos['x'])
                y_list.append(pos['y'])
            drawing.append([x_list, y_list])
        drawing = normalize_resample_simplify(drawing)
        cnt = 0
        for i in range(len(drawing)):
            t_list = []
            for j in range((len(drawing[i][0]))):
                t_list.append(cnt)
                cnt += 1
            drawing[i].append(t_list)

        global pred
        pred = test_person(drawing)
        pred = json.dumps(pred)
        return HttpResponse(pred)
    return HttpResponse("OK")
