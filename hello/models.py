from djongo import models


class Measurement(models.Model):
    number = models.IntegerField()
    air_pressure_9am = models.DecimalField(decimal_places=12, max_digits=19)
    air_temp_9am = models.DecimalField(decimal_places=12, max_digits=19)
    avg_wind_direction_9am = models.DecimalField(decimal_places=12, max_digits=19)
    avg_wind_speed_9am = models.DecimalField(decimal_places=12, max_digits=19)
    max_wind_direction_9am = models.DecimalField(decimal_places=12, max_digits=19)
    max_wind_speed_9am = models.DecimalField(decimal_places=12, max_digits=19)
    rain_accumulation_9am = models.DecimalField(decimal_places=12, max_digits=19)
    rain_duration_9am = models.DecimalField(decimal_places=12, max_digits=19)
    relative_humidity_9am = models.DecimalField(decimal_places=12, max_digits=19)
    relative_humidity_3pm = models.DecimalField(decimal_places=12, max_digits=19)
    dataset_name = models.TextField()

