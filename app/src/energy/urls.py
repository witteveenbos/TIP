from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from energy import views

urlpatterns = [
    # calculate
    path(
        "options/area_division/",
        views.options_area_division,
        name="AreaDivision options",
    ),
    path("geojsons/", views.area_division_geojsons, name="GeoJSON for area divisions"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
