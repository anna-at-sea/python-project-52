from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class Label(models.Model):
    name = models.CharField(max_length=150, blank=False, verbose_name=_("Name"))
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.task_set.exists():
            raise ValidationError(
                "This label cannot be deleted."
            )
        super().delete(*args, **kwargs)
