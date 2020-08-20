from django.shortcuts import render
from django.http import HttpResponse

from .models import Measurement
import csv
from decimal import Decimal
from rest_framework import routers, serializers, viewsets

# Create your views here.
def index(request):
    return render(request, "index.html")


def db(request):
    return render(request, "db.html", {"measurements": []})


def upload_form(request):
    return render(request, 'upload.html')


def upload_measurements(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        decoded_file = file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file, delimiter=';')
        first = next(reader)
        all = []
        for row in reader:
            data = dict(zip(first, row))
            data = {key: value.replace(',', '.') for key, value in data.items()}
            d = {key: Decimal(value) if key != 'number' else int(value) for key, value in data.items() if value}
            m = Measurement(dataset_name='felipe', **d)
            all += (m, )

        Measurement.objects.bulk_create(all, batch_size=10)
        return HttpResponse('Upload successful!')


class MeasurementSerializer(serializers.Serializer):
    air_pressure_9am = serializers.DecimalField(decimal_places=12, max_digits=19)
    air_temp_9am = serializers.DecimalField(decimal_places=12, max_digits=19)
    avg_wind_direction_9am = serializers.DecimalField(decimal_places=12, max_digits=19)
    avg_wind_speed_9am = serializers.DecimalField(decimal_places=12, max_digits=19)
    max_wind_direction_9am = serializers.DecimalField(decimal_places=12, max_digits=19)
    max_wind_speed_9am = serializers.DecimalField(decimal_places=12, max_digits=19)
    rain_accumulation_9am = serializers.DecimalField(decimal_places=12, max_digits=19)
    rain_duration_9am = serializers.DecimalField(decimal_places=12, max_digits=19)
    relative_humidity_9am = serializers.DecimalField(decimal_places=12, max_digits=19)
    relative_humidity_3pm = serializers.DecimalField(decimal_places=12, max_digits=19)
    dataset_name = serializers.CharField()
    number = serializers.IntegerField()

    class Meta:
        model = Measurement


class MeasurementsViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
