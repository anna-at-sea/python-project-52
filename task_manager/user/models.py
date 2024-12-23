from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    class Meta:
        verbose_name = "User"

    first_name = models.CharField(
        max_length=150, blank=False, verbose_name=_("First Name")
    )
    last_name = models.CharField(
        max_length=150, blank=False, verbose_name=_("Last Name")
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
