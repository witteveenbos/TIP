import json
import requests
import os
from pathlib import Path

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from energy.models import (
    AreaDivision,
    MunicipalityIDs,
    ProvinceIDs,
    RegionIDs,
)

GeoID = [*RegionIDs.choices, *MunicipalityIDs.choices, *ProvinceIDs.choices]
STATIC_FOLDER = Path(__file__).parent / "static"


# map options
@api_view(["GET"])
def options_area_division(request):
    return Response(
        [
            {"value": area_div.value, "label": area_div.label}
            for area_div in AreaDivision
        ],
        status=status.HTTP_200_OK,
    )


# map options
@api_view(["GET"])
def area_division_geojsons(request):
    file_paths = {
        AreaDivision.REG: STATIC_FOLDER / "shapes" / "regions.geojson",
        AreaDivision.PROV: STATIC_FOLDER / "shapes" / "province.geojson",
        AreaDivision.GM: STATIC_FOLDER / "shapes" / "municipalities.geojson",
        AreaDivision.RES: STATIC_FOLDER / "shapes" / "res.geojson",
        AreaDivision.HSMS: STATIC_FOLDER / "shapes" / "hsms.geojson",
    }

    data = {}
    for label, path in file_paths.items():
        with open(path, "r") as file:
            data[label] = json.load(file)

    return JsonResponse(data)
