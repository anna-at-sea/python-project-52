from django.forms import ModelForm

from .models import Label


class LabelForm(ModelForm):

    class Meta:
        model = Label
        fields = ['name']

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label
