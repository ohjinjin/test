from django.shortcuts import render
from django.http import HttpResponse
from .fusioncharts import FusionCharts
from collections import OrderedDict

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request,'about.html')

def result(request):
    text = request.GET['fulltext']

    words = text.split()
    word_dictionary = {}

    for word in words:
        if word in word_dictionary:
            word_dictionary[word]+=1
        else:
            word_dictionary[word]=1

    # 차트 데이터는 키 - 값 쌍 형태의 사전으로 'dataSource` 매개 변수에 전달됩니다.
    dataSource = OrderedDict()

    # 'chartConfig` dict는 차트 속성에 대한 키 - 값 쌍 데이터를 포함합니다
    chartConfig = OrderedDict()
    chartConfig["caption"] = "Frequency of words"
    chartConfig["subCaption"] = "Frequency of each word in the input text"
    chartConfig["xAxisName"] = "Word"
    chartConfig["yAxisName"] = "Frequency"
    chartConfig["numberSuffix"] = ""
    chartConfig["theme"] = "fusion"

    # `chartData` dict에는 키 - 값 쌍 데이터가 들어 있습니다
    chartData = OrderedDict()
    
    for word in words:
        chartData[word] = word_dictionary[word]

    dataSource["chart"] = chartConfig
    dataSource["data"] = []
    
    # `chartData` 배열의 데이터를 FusionCharts가 소비 할 수있는 형식으로 변환하십시오.
    # 차트의 데이터는 배열에 있어야하며 배열의 각 요소는 JSON 객체입니다.
    #`label`과`value`를 키로 사용합니다

    # `chartData`의 데이터를 반복하고`dataSource [ 'data']`리스트에 삽입하십시오
    for key, value in chartData.items():
        data = {}
        data["label"] = key
        data["value"] = value
        dataSource["data"].append(data)


    # FusionCharts 클래스 생성자를 사용하여 열 2D 차트의 개체를 만듭니다.
    # 차트 데이터는`dataSource` 매개 변수에 전달됩니다
    column2D = FusionCharts("column2d", "myFirstChart" , "650", "400", "myFirstchart-container", "json", dataSource)
    
    return render(request,'result.html',{'output' : column2D.render(),'full':text,'total':len(words),'dictionary':word_dictionary.items})
