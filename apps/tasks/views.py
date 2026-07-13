from datetime import datetime

from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .utils import create_task_history
from .models import Task, TaskHistory
from .serializers import (
    TaskSerializer,
    MoveTaskSerializer,
    TaskHistorySerializer,
)

from .models import Task
from .serializers import (
    TaskSerializer,
    MoveTaskSerializer,
)

class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Task.objects.filter(owner=self.request.user)

        date = self.request.query_params.get("date")

        if date:
            queryset = queryset.filter(due_date=date)

        return queryset

    def perform_create(self, serializer):
        status = serializer.validated_data.get(
            "status",
            Task.Status.TODO,
        )

        last_position = (
            Task.objects.filter(
                owner=self.request.user,
                status=status,
            ).count()
        )

        task = serializer.save(
            owner=self.request.user,
            position=last_position,
        )

        create_task_history(
            owner=self.request.user,
            action="created",
            task=task,
            task_title=task.title,
        )

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(
            owner=self.request.user
        )

    def perform_update(self, serializer):
        task = self.get_object()

        old_data = {
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "due_date": str(task.due_date),
            "tags": task.tags,
        }

        old_status = task.status

        updated_task = serializer.save()

        # Handle drag-and-drop separately
        if old_status != updated_task.status:
            create_task_history(
                owner=self.request.user,
                action="moved",
                task=updated_task,
                task_title=updated_task.title,
                details={
                    "from_status": old_status,
                    "to_status": updated_task.status,
                },
            )
            return

        new_data = {
            "title": updated_task.title,
            "description": updated_task.description,
            "priority": updated_task.priority,
            "due_date": str(updated_task.due_date),
            "tags": updated_task.tags,
        }

        changes = {}

        for field in old_data:
            if old_data[field] != new_data[field]:
                changes[field] = {
                    "old": old_data[field],
                    "new": new_data[field],
                }

        if changes:
            create_task_history(
                owner=self.request.user,
                action="updated",
                task=updated_task,
                task_title=updated_task.title,
                details=changes,
            )

    def perform_destroy(self, instance):
        create_task_history(
            owner=self.request.user,
            action="deleted",
            task_title=instance.title,
        )

        instance.delete()

class TaskHistoryListView(generics.ListAPIView):
    serializer_class = TaskHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            TaskHistory.objects.filter(
                owner=self.request.user
            )
            .select_related("task")
            .order_by("-created_at")
        )

@api_view(["PATCH"])
@permission_classes([permissions.IsAuthenticated])
def move_task(request, pk):
    try:
        task = Task.objects.get(
            pk=pk,
            owner=request.user,
        )
    except Task.DoesNotExist:
        return Response(
            {"detail": "Task not found."},
            status=status.HTTP_404_NOT_FOUND,
        )
    
    old_status = task.status
    old_position = task.position

    serializer = MoveTaskSerializer(
        task,
        data=request.data,
        partial=True,
    )

    print("REQUEST:", request.data)
    print("BEFORE:", task.status)

    serializer.is_valid(raise_exception=True)

    print("VALIDATED:", serializer.validated_data)

    if "status" in serializer.validated_data:
        task.status = serializer.validated_data["status"]

    if "position" in serializer.validated_data:
        task.position = serializer.validated_data["position"]

    task.save()

    if (
        old_status != task.status
        or old_position != task.position
    ):
        create_task_history(
            owner=request.user,
            action="moved",
            task=task,
            task_title=task.title,
            details={
                "from_status": old_status,
                "to_status": task.status,
                "from_position": old_position,
                "to_position": task.position,
            },
        )

    task.refresh_from_db()

    print("AFTER:", task.status)

    return Response(
        TaskSerializer(task).data
    )