from django.shortcuts import render
from django.http import HttpResponse

from .models import Measurement
import csv
from rest_framework import routers, serializers, viewsets
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
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
            all += (m, )

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

    class Meta:
        model = Measurement


class MeasurementsViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer


def aggregate_avg_wind_direction_9am(request):
    cursor = Measurement.objects.mongo_aggregate([{
        '$bucket': {
            'groupBy': '$avg_wind_direction_9am',
            'boundaries': [n * 45 - 3 * 45 / 2 for n in range(1, 10)],
            'default': -1000,
            'output': {
                'outputN': {'$sum': 1}
            }
        }
    }])
    result = [d for d in cursor]
    result = {r['_id']: r['outputN'] for r in result}
    return HttpResponse(json.dumps(result))
