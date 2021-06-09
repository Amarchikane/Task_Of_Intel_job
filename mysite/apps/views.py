from django.shortcuts import render
from django.http import HttpResponse, request

# Create your views here.
# import urllib library
from urllib.request import urlopen

# import json
import json
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from datetime import datetime
from _datetime import timedelta
# store the URL in url as
# parameter for urlopen
url = "https://data.cityofchicago.org/resource/k7hf-8y75.json"

# store the response of URL
response = urlopen(url)

# storing the JSON response
# from url in data
data_json = json.loads(response.read())
Temperature=[]
Humidity=[]
Wind_Speed=[]
measurement_timestamp_label=[]
now = datetime.now()
temp=""

def test(request):

    global temp
    global Temperature
    global Humidity
    global Wind_Speed
    global measurement_timestamp_label
    global data_json
    Temperature=[]
    Humidity=[]
    Wind_Speed=[]
    measurement_timestamp_label=[]
    dd=0
    mm=0
    hh=6
    dt_string = '2021-06-07T15:00:00.000'
    date_1 = datetime.strptime(dt_string, '%Y-%m-%dT%H:%M:%S.%f')
    if request.POST.get('quantity') or request.POST.get('quantity1') or request.POST.get('quantity2'):
        if  request.POST.get('quantity'):
            dd=int(request.POST.get('quantity'))
        if  request.POST.get('quantity2'):
            mm=int(request.POST.get('quantity2'))
        if  request.POST.get('quantity1'):
            hh=int(request.POST.get('quantity1'))
        end_date=date_1 - timedelta(days=dd,hours=hh,minutes=mm)
    else:
        end_date = date_1 - timedelta(hours=6)
    end_date=end_date.strftime('%Y-%m-%dT%H:%M:%S.%f')
    date_time_obj3 = datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%S.%f')
    date_time_obj=datetime.strptime(dt_string, '%Y-%m-%dT%H:%M:%S.%f')
    date_time_obj3=datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%S.%f')
    if request.method=="POST":
        if request.POST.get('Station')=="1":
            temp="Oak Street Weather Station"
        else:
            temp="Foster Weather Station"
        # print("run",Country)  
    for i in data_json:
        if i['station_name']==temp:
            
            date_time_obj2=datetime.strptime(i['measurement_timestamp'], '%Y-%m-%dT%H:%M:%S.%f')
            
            if date_time_obj>=date_time_obj2 and date_time_obj2>=date_time_obj3:
                measurement_timestamp_label.append(i['measurement_timestamp_label'])
                Temperature.append(i['air_temperature']) 
                Humidity.append(i['humidity']) 
                Wind_Speed.append(i['wind_speed']) 
    line_chart = TemplateView.as_view(template_name='line_chart.html')
    line_chart_json = LineChartJSONView.as_view()
    return render(request,'test.html',{'graph':temp,'startDate':str(date_time_obj),'enddate':str(date_time_obj3),'hh':hh,'mm':mm,'dd':dd})

class LineChartJSONView(BaseLineChartView):

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return measurement_timestamp_label

    def get_providers(self):
        """Return names of datasets."""
        return ["Temperature", "Humidity", "Wind_Speed"]

    def get_data(self):
        """Return 3 datasets to plot."""

        return [Temperature,
                Humidity,
                Wind_Speed]


line_chart = TemplateView.as_view(template_name='line_chart.html')
line_chart_json = LineChartJSONView.as_view()