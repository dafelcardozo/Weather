from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

import hello.views


urlpatterns = [
    path("", hello.views.index, name="index"),
    path("db/", hello.views.db, name="db"),
    path("admin/", admin.site.urls),
    path("upload", hello.views.upload_form),
    path("upload_measurements", hello.views.upload_measurements),
    path('all', hello.views.MeasurementsViewSet.as_view({'get': 'list'})),
    path('wind_direction_aggregates', hello.views.wind_direction_aggregates),
    path('available_months', hello.views.available_months),
    path('measurements', hello.views.monthly_measurements),
    path('today_prediction', hello.views.today_prediction)
]
