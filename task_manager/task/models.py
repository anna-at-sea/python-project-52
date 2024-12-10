from django.db import models
from django.utils import timezone
from task_manager.status.models import Status
from task_manager.user.models import User
# from task_manager.label.models import Label


class Task(models.Model):
    name = models.CharField(max_length=150, blank=False)
    description = models.TextField(blank=True, null=True)
    status = models.ForeignKey(Status, blank=False, on_delete=models.PROTECT)
    creator = models.ForeignKey(
        User, related_name="created_tasks",
        blank=False, on_delete=models.PROTECT
    )
    executor = models.ForeignKey(
        User, related_name="executed_tasks",
        blank=True, null=True, on_delete=models.PROTECT
    )
    created_at = models.DateTimeField(default=timezone.now)
    # labels = models.ManyToManyField(Label, blank=True)

    def __str__(self):
        return self.name
