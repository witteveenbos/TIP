from django.db import transaction
from django.db.models import F
from django.utils import timezone
from rest_framework import generics, permissions, serializers
from rest_framework.response import Response
from rest_framework import status

from .models import WorkboardItems
from .workboard_serializers import (
    WorkboardItemLaneSerializer,
    WorkboardItemPositionSerializer,
    WorkboardItemsSerializer,
)


class WorkboardItemsByPageList(generics.ListCreateAPIView):
    serializer_class = WorkboardItemsSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        return WorkboardItems.objects.filter(page_id=self.kwargs["page_id"])

    def perform_create(self, serializer):
        with transaction.atomic():
            items = WorkboardItems.objects.select_for_update().filter(
                page_id=self.kwargs["page_id"], lane=0
            )
            items.update(sort_order=F("sort_order") + 1)
            serializer.save(
                page_id=self.kwargs["page_id"],
                lane=0,
                sort_order=0,
                organization=getattr(self.request.user, "organization", ""),
                updated_by=self.request.user,
            )


class WorkboardItemLaneUpdate(generics.UpdateAPIView):
    queryset = WorkboardItems.objects.all()
    serializer_class = WorkboardItemLaneSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["patch"]

    def update(self, request, *args, **kwargs):
        item = self.get_object()
        user_organization = getattr(request.user, "organization", "")
        if item.organization != user_organization:
            return Response(
                {"detail": "You cannot move items from another organization."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=request.user)
        return Response(serializer.data)


class WorkboardItemPositionUpdate(generics.UpdateAPIView):
    queryset = WorkboardItems.objects.all()
    serializer_class = WorkboardItemPositionSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["patch"]

    def update(self, request, *args, **kwargs):
        item = self.get_object()
        user_organization = getattr(request.user, "organization", "")
        if item.organization != user_organization:
            return Response(
                {"detail": "You cannot move items from another organization."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        with transaction.atomic():
            item = WorkboardItems.objects.select_for_update().get(pk=item.pk)
            target_lane = data["lane"]
            target_item_id = data.get("target_item_id")
            lane_items = list(
                WorkboardItems.objects.select_for_update()
                .filter(page_id=item.page_id, lane__in={item.lane, target_lane})
                .order_by("lane", "sort_order", "id")
            )
            target_item = next(
                (
                    lane_item
                    for lane_item in lane_items
                    if lane_item.id == target_item_id
                ),
                None,
            )
            if target_item_id == item.id:
                raise serializers.ValidationError(
                    {"target_item_id": "Target item must be different from the moved item."}
                )
            if target_item_id is not None and (
                target_item is None or target_item.lane != target_lane
            ):
                raise serializers.ValidationError(
                    {"target_item_id": "Target item must be in the destination lane."}
                )

            items_by_lane = {
                lane: [
                    lane_item
                    for lane_item in lane_items
                    if lane_item.lane == lane and lane_item.id != item.id
                ]
                for lane in {item.lane, target_lane}
            }
            destination_items = items_by_lane[target_lane]
            if target_item_id is None:
                destination_items.append(item)
            else:
                target_index = next(
                    index
                    for index, lane_item in enumerate(destination_items)
                    if lane_item.id == target_item_id
                )
                insert_index = target_index + (
                    0 if data["insert_before"] else 1
                )
                destination_items.insert(insert_index, item)

            now = timezone.now()
            items_to_update = []
            for lane, lane_items in items_by_lane.items():
                for sort_order, lane_item in enumerate(lane_items):
                    lane_item.lane = lane
                    lane_item.sort_order = sort_order
                    if lane_item.id == item.id:
                        lane_item.updated_by = request.user
                        lane_item.updated_at = now
                    items_to_update.append(lane_item)
            WorkboardItems.objects.bulk_update(
                items_to_update,
                ["lane", "sort_order", "updated_by", "updated_at"],
            )

        return Response(WorkboardItemsSerializer(item).data)
