from rest_framework import serializers

from .models import WorkboardItems


class WorkboardItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkboardItems
        fields = [
            "id",
            "title",
            "description",
            "organization",
            "type",
            "size_mw",
            "status",
            "acm_prio",
            "page_id",
            "lane",
            "updated_by",
            "updated_at",
        ]


class WorkboardItemLaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkboardItems
        fields = ["lane"]
