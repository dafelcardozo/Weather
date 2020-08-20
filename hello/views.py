from django.shortcuts import render
from django.http import HttpResponse

from .models import Measurement
import csv
from decimal import Decimal
from rest_framework import routers, serializers, viewsets
from django.views.decorators.csrf import csrf_exempt

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
            d = {key: Decimal(value) if key != 'number' else int(value) for key, value in data.items() if value}
            m = Measurement(dataset_name=name, **d)
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
