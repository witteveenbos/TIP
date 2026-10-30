from rest_framework import serializers

from .models import WorkboardItemModification, WorkboardItems


class WorkboardItemsSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.secret != 1:
            return data

        request = self.context.get("request")
        user = getattr(request, "user", None)
        if user and user.is_authenticated and (
            user.is_staff
            or user.is_superuser
            or (
                instance.organization
                and instance.organization == getattr(user, "organization", "")
            )
        ):
            return data

        return {
            "id": data["id"],
            "lane": data["lane"],
            "title": "Vertrouwelijk project",
            "size_mw": data["size_mw"],
            "organization": data["organization"],
        }

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
            "secret",
            "page_id",
            "lane",
            "sort_order",
            "updated_by",
            "updated_at",
        ]
        read_only_fields = ["sort_order"]


class WorkboardItemUpdateSerializer(serializers.ModelSerializer):
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
            "secret",
            "page_id",
            "lane",
            "sort_order",
            "updated_by",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "organization",
            "page_id",
            "lane",
            "sort_order",
            "updated_by",
            "updated_at",
        ]


class WorkboardItemModificationSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = WorkboardItemModification
        fields = [
            "id",
            "change_type",
            "changed_fields",
            "updated_at",
            "updated_by",
            "username",
        ]

    def get_username(self, modification):
        return (
            modification.updated_by.get_username()
            if modification.updated_by
            else None
        )


class WorkboardItemLaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkboardItems
        fields = ["lane"]


class WorkboardItemPositionSerializer(serializers.Serializer):
    lane = serializers.IntegerField()
    target_item_id = serializers.IntegerField(allow_null=True, required=False)
    insert_before = serializers.BooleanField(default=False)
