from rest_framework import serializers

from .models import Task, TaskHistory


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.id")

    class Meta:
        model = Task
        fields = (
            "id",
            "owner",
            "title",
            "description",
            "status",
            "priority",
            "due_date",
            "tags",
            "position",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "owner",
            "created_at",
            "updated_at",
        )

class MoveTaskSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=Task.Status.choices,
        required=False
    )

    position = serializers.IntegerField(
        min_value=0,
        required=False
    )

class TaskHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskHistory
        fields = "__all__"