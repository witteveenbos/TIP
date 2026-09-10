from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status

from .models import WorkboardItems
from .workboard_serializers import (
    WorkboardItemLaneSerializer,
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
        serializer.save(
            page_id=self.kwargs["page_id"],
            lane=0,
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
