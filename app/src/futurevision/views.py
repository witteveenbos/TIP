import json

from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from energy.models import ProvinceIDs, RegionIDs

from .models import FutureVision
from .serializers import FutureVisionSerializer, FutureVisionWithoutDataSerializer


class FutureVisionList(generics.ListCreateAPIView):
    queryset = FutureVision.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return FutureVisionWithoutDataSerializer
        elif self.request.method == "POST":
            return FutureVisionSerializer


class FutureVisionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FutureVisionSerializer
    queryset = FutureVision.objects.all()


@api_view(["POST"])
def combine_future_visions(request):
    if (
        "name" not in request.data
        or "geo_id" not in request.data
        or "scenario" not in request.data
        or request.data.get("geo_id") not in ProvinceIDs.values
    ):
        return Response(
            {"error": "Invalid data format"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Retrieve future visions to combine
    selected_future_vision_ids = [request.data.get(key) for key in RegionIDs.values]
    future_visions = FutureVision.objects.filter(id__in=selected_future_vision_ids)

    combined_json_data = []
    region_muncipality_hierarchy = EnergyUnit.get_region_hierarchy()
    for future_vision in future_visions:
        json_data = json.loads(future_vision.json_data)
        region_id = future_vision.geo_id
        muncipalities = set(region_muncipality_hierarchy[region_id])

        # Cut jsondata to only include muncipalities of the selected region
        cut_json_data = [
            development
            for development in json_data
            if development["gid"] in muncipalities
        ]
        combined_json_data.extend(cut_json_data)

    combined_future_vision = FutureVision(
        name=request.data["name"],
        geo_id=request.data["geo_id"],
        scenario=request.data["scenario"],
        json_data=json.dumps(combined_json_data),
    )
    combined_future_vision.save()

    serializer = FutureVisionSerializer(combined_future_vision)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
