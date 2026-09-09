from rest_framework import serializers

from . import SwimmingLane, WorkboardPage
from .base_serializer import BasePageSerializer


class SwimmingLaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = SwimmingLane
        fields = [
            "label",
            "minimum_energy",
            "maximum_energy",
            "minimum_risk",
            "maximum_risk",
        ]


class WorkboardPageSerializer(BasePageSerializer):
    swimming_lanes = SwimmingLaneSerializer(many=True)

    class Meta:
        model = WorkboardPage
        fields = BasePageSerializer.Meta.fields + [
            "id",
            "phase",
            "swimming_lanes",
        ]
