from django.db import models
from django.utils import timezone
from task_manager.status.models import Status
from task_manager.user.models import User
from task_manager.label.models import Label
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    name = models.CharField(
        max_length=150, blank=False, verbose_name=_("Name")
    )
    description = models.TextField(
        blank=True, null=True, verbose_name=_("Description")
    )
    status = models.ForeignKey(
        Status, blank=False, on_delete=models.PROTECT, verbose_name=_("Status")
    )
    creator = models.ForeignKey(
        User, related_name="created_tasks",
        blank=False, on_delete=models.PROTECT
    )
    executor = models.ForeignKey(
        User, related_name="executed_tasks",
        blank=True, null=True, on_delete=models.PROTECT,
        verbose_name=_("Executor")
    )
    created_at = models.DateTimeField(default=timezone.now)
    labels = models.ManyToManyField(
        Label, blank=True, verbose_name=_("Labels")
    )

    def __str__(self):
        return self.name
