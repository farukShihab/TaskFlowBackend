from django.urls import path

from .views import (
    TaskListCreateView,
    TaskDetailView,
    TaskHistoryListView,
    move_task,
)

urlpatterns = [
    path(
        "",
        TaskListCreateView.as_view(),
        name="task-list",
    ),
    path(
        "<int:pk>/",
        TaskDetailView.as_view(),
        name="task-detail",
    ),
    path(
        "<int:pk>/move/",
        move_task,
        name="task-move",
    ),
    path(
        "history/",
        TaskHistoryListView.as_view(),
        name="task-history",
    ),
]