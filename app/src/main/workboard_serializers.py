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
            "sort_order",
            "updated_by",
            "updated_at",
        ]
        read_only_fields = ["sort_order"]


class WorkboardItemLaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkboardItems
        fields = ["lane"]


class WorkboardItemPositionSerializer(serializers.Serializer):
    lane = serializers.IntegerField()
    target_item_id = serializers.IntegerField(allow_null=True, required=False)
    insert_before = serializers.BooleanField(default=False)
