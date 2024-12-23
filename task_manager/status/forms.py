from django.contrib.auth.forms import ValidationError
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Status


class StatusForm(ModelForm):

    class Meta:
        model = Status
        fields = ['name']

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if self._meta.model.objects.filter(
            name=name
        ).exclude(pk=self.instance.pk).exists():
            raise ValidationError(
                _("Task status with this name already exists.")
            )
        return name
