from django.urls import path

from .workboard_views import (
    WorkboardItemLaneUpdate,
    WorkboardItemPositionUpdate,
    WorkboardItemsByPageList,
)


urlpatterns = [
    path("<int:page_id>/", WorkboardItemsByPageList.as_view(),
         name="workboard items"),
    path("item/<int:pk>/lane/", WorkboardItemLaneUpdate.as_view(),
         name="workboard item lane"),
    path("item/<int:pk>/position/", WorkboardItemPositionUpdate.as_view(),
         name="workboard item position"),
]
