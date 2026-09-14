from django.urls import path

from .workboard_views import (
    WorkboardItemLaneUpdate,
    WorkboardItemModificationList,
    WorkboardItemPositionUpdate,
    WorkboardItemUpdate,
    WorkboardItemsByPageList,
)


urlpatterns = [
    path("<int:page_id>/", WorkboardItemsByPageList.as_view(),
         name="workboard items"),
    path("item/<int:pk>/lane/", WorkboardItemLaneUpdate.as_view(),
         name="workboard item lane"),
    path("item/<int:pk>/modifications/", WorkboardItemModificationList.as_view(),
         name="workboard item modifications"),
    path("item/<int:pk>/", WorkboardItemUpdate.as_view(),
         name="workboard item update"),
    path("item/<int:pk>/position/", WorkboardItemPositionUpdate.as_view(),
         name="workboard item position"),
]
