from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status

from .models import WorkboardItems
from .workboard_serializers import (
    WorkboardItemLaneSerializer,
    WorkboardItemsSerializer,
)


class WorkboardItemsByPageList(generics.ListAPIView):
    serializer_class = WorkboardItemsSerializer

    def get_queryset(self):
        return WorkboardItems.objects.filter(page_id=self.kwargs["page_id"])


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
