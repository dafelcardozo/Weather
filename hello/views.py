from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import Measurement
import csv
from rest_framework import serializers, viewsets
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta


def index(request):
    return render(request, "index.html")


def db(request):
    return render(request, "db.html", {"measurements": []})


def upload_form(request):
    return render(request, 'upload.html')


@csrf_exempt
def upload_measurements(request):
    if request.method == 'POST' and request.FILES['file']:
        name = request.POST['name']
        column_delimiter = request.POST['column_delimiter']
        decimal_separator = request.POST['decimal_separator']
        file = request.FILES['file']
        decoded_file = file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file, delimiter=column_delimiter)
        first = next(reader)
        all = []
        for row in reader:
            data = dict(zip(first, row))
            data = {key: value.replace(decimal_separator, '.') for key, value in data.items()}
            d = {key: float(value) if key != 'number' else int(value) for key, value in data.items() if value}
            m = Measurement(dataset_name=name, **d)
            all += (m,)

        current_date = date(2011, 9, 14)
        for m in all:
            m.date = current_date
            current_date += timedelta(days=1)
        Measurement.objects.bulk_create(all, batch_size=10)
        return HttpResponse('Upload successful!')


class MeasurementSerializer(serializers.Serializer):
    air_pressure_9am = serializers.FloatField()
    air_temp_9am = serializers.FloatField()
    avg_wind_direction_9am = serializers.FloatField()
    avg_wind_speed_9am = serializers.FloatField()
    max_wind_direction_9am = serializers.FloatField()
    max_wind_speed_9am = serializers.FloatField()
    rain_accumulation_9am = serializers.FloatField()
    rain_duration_9am = serializers.FloatField()
    relative_humidity_9am = serializers.FloatField()
    relative_humidity_3pm = serializers.FloatField()
    dataset_name = serializers.CharField()
    number = serializers.IntegerField()
    date = serializers.DateField()

    class Meta:
        model = Measurement


class MeasurementsViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer


def wind_direction_aggregate(month, year, field):
    cursor = Measurement.objects.mongo_aggregate([
        {
            '$project': {
                'year': {
                    '$year': "$date",
                },
                'month': {
                    '$month': '$date'
                },
                'avg_wind_direction_9am': '$avg_wind_direction_9am'
            }
        },
        {
            '$match': {"year": year, 'month': month}
        },
        {
            '$bucket': {
                'groupBy': '$' + field,
                'boundaries': [n * 45 - 3 * 45 / 2 for n in range(1, 9)],
                'default': -1000,
                'output': {
                    'outputN': {'$sum': 1}
                }
            }
        }
    ])
    return {r['_id']: r['outputN'] for r in cursor}


def wind_direction_aggregates(request):
    month, year = int(request.GET['month']), int(request.GET['year'])
    datasets = dict(avg_wind_direction_9am=wind_direction_aggregate(month, year, 'avg_wind_direction_9am'),
                    max_wind_direction_9am=wind_direction_aggregate(month, year, 'max_wind_direction_9am'))
    return HttpResponse(json.dumps(datasets))


def available_months(request):
    cursor = Measurement.objects.mongo_aggregate([{
        '$group': {
            '_id': {'month': {'$month': "$date"}, 'year': {'$year': '$date'}},
            'count_measurements': {'$sum': 1}
        }
    }])
    months = [(m['_id']['month'], m['_id']['year']) for m in cursor]
    result = [(year, month, date(year, month, 1).strftime('%B %Y')) for month, year in months]
    return HttpResponse(json.dumps(result))


def monthly_measurements(request):
    month, year = int(request.GET['month']), int(request.GET['year'])
    start = date(year, month, 1)
    measurements = Measurement.objects.filter(date__gte=start, date__lt=start + relativedelta(months=+1))
    return JsonResponse(MeasurementSerializer(measurements, many=True).data, safe=False)
