from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    name = models.CharField(
        max_length=150, unique=True, blank=False, verbose_name=_("Name"),
        error_messages={
            'unique': _("Label with this name already exists.")
        }
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        # Если убрать этот блок, тогда можно будет удалить Label, когда он
        # привязан к Task, тесты это подтверждают. Для ManyToManyField же нельзя
        # использовать on_delete=models.PROTECT, как для других полей? Есть
        # другой способ запретить удаление в модели Task?
        if self.task_set.exists():
            raise ValidationError(
                "This label cannot be deleted."
            )
        super().delete(*args, **kwargs)
