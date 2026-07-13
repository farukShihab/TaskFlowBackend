from .models import TaskHistory

def create_task_history(
    *,
    owner,
    action,
    task_title,
    task=None,
    details=None,
):
    TaskHistory.objects.create(
        owner=owner,
        action=action,
        task=task,
        task_title=task_title,
        details=details or {},
    )