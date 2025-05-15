from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from futurevision import views

urlpatterns = [
    path("", views.FutureVisionList.as_view(), name="future vision list"),
    path("<int:pk>/", views.FutureVisionDetail.as_view(), name="future vision detail"),
    path("combine/", views.combine_future_visions, name="combine future visions"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
