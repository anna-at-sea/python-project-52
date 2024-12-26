from django.forms import ModelForm

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
