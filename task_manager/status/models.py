from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    name = models.CharField(max_length=150, blank=False, verbose_name=_("Name"))
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
