from django.urls import path

from .workboard_views import WorkboardItemLaneUpdate, WorkboardItemsByPageList


urlpatterns = [
    path("<int:page_id>/", WorkboardItemsByPageList.as_view(),
         name="workboard items"),
    path("item/<int:pk>/lane/", WorkboardItemLaneUpdate.as_view(),
         name="workboard item lane"),
]
