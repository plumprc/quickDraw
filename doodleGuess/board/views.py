from django.shortcuts import HttpResponse, render
import json
import pandas as pd

# Create your views here.


def draw(request):
    return render(request, 'index.html')


def process(request):
    # print(request.POST['data'])
    data = json.loads(request.body)
    cnt = 0
    drawing = []
    for i in range(len(data)):
        x_list = []
        y_list = []
        t_list = []
        for pos in data[i]:
            x_list.append(pos['x'])
            y_list.append(pos['y'])
            t_list.append(cnt * 0.1)
            cnt = cnt + 1
        drawing.append([x_list, y_list, t_list])

    df = pd.DataFrame({'key_id': cnt, 'countrycode': 'CN', 'drawing': str(drawing)}, index=[2])
    df.to_csv("myDraw.csv", mode='a')
    return HttpResponse("OK")
