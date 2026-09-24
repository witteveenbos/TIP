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
    is_admin = serializers.SerializerMethodField()

    def get_is_admin(self, page):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        return bool(
            user
            and user.is_authenticated
            and (user.is_staff or user.is_superuser)
        )

    class Meta:
        model = WorkboardPage
        fields = BasePageSerializer.Meta.fields + [
            "id",
            "phase",
            "is_admin",
            "swimming_lanes",
        ]
