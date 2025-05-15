from rest_framework import serializers
from .models import FutureVision


class FutureVisionSerializer(serializers.ModelSerializer):
    geo_id_label = serializers.SerializerMethodField()

    class Meta:
        model = FutureVision
        fields = "__all__"

    def get_scenario_label(self, obj):
        return obj.get_scenario_display()

    def get_geo_id_label(self, obj):
        return obj.get_geo_id_display()


class FutureVisionWithoutDataSerializer(serializers.ModelSerializer):
    geo_id_label = serializers.SerializerMethodField()

    class Meta:
        model = FutureVision
        exclude = ["json_data"]

    def get_scenario_label(self, obj):
        return obj.get_scenario_display()

    def get_geo_id_label(self, obj):
        return obj.get_geo_id_display()
