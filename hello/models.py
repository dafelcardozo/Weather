from djongo import models


class Measurement(models.Model):
    number = models.IntegerField()
    air_pressure_9am = models.FloatField()
    air_temp_9am = models.FloatField()
    avg_wind_direction_9am = models.FloatField()
    avg_wind_speed_9am = models.FloatField()
    max_wind_direction_9am = models.FloatField()
    max_wind_speed_9am = models.FloatField()
    rain_accumulation_9am = models.FloatField()
    rain_duration_9am = models.FloatField()
    relative_humidity_9am = models.FloatField()
    relative_humidity_3pm = models.FloatField()
    dataset_name = models.TextField()
    date = models.DateField()

    objects = models.DjongoManager()

# from django.db.models import Case, IntegerField, Value, When
# Measurement.objects.annotate(count=Case(When(avg_wind_direction_9am__lt=45, then=Value(1)), default=Value(2), output_field=IntegerField()))
