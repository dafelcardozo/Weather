from django.shortcuts import render
from django.http import HttpResponse
from django.db import transaction

from .models import Measurement
import csv
from decimal import Decimal

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")


def db(request):

    greeting = Measurement()
    greeting.save()

    greetings = Measurement.objects.all()

    return render(request, "db.html", {"measurements": greetings})


def upload_form(request):
    return render(request, 'upload.html')


@transaction.atomic
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

        Measurement.objects.bulk_create(all)
        return HttpResponse('Upload successful!')