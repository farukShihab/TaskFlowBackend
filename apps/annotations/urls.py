from django.urls import path

from .views import (
    StudyListCreateView,
    StudyRetrieveView,
    StudyDeleteView,
    StudyImageUploadView,
    PolygonCreateView,
    PolygonUpdateView,
    PolygonDeleteView,
)

urlpatterns = [
    path(
        "",
        StudyListCreateView.as_view(),
    ),

    path(
        "<int:pk>/",
        StudyRetrieveView.as_view(),
    ),

    path(
        "<int:pk>/delete/",
        StudyDeleteView.as_view(),
    ),

    path(
        "<int:study_id>/images/",
        StudyImageUploadView.as_view(),
    ),

    path(
        "images/<int:image_id>/polygons/",
        PolygonCreateView.as_view(),
    ),

    path(
        "polygons/<int:pk>/",
        PolygonUpdateView.as_view(),
    ),

    path(
        "polygons/<int:pk>/delete/",
        PolygonDeleteView.as_view(),
    ),
]