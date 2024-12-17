from django.contrib.auth.forms import UserCreationForm, ValidationError
from django.forms import CharField, PasswordInput
from django.utils.translation import gettext_lazy as _

from .models import User


class UserForm(UserCreationForm):
    password1 = CharField(
        label=_("Password"),
        widget=PasswordInput,
        help_text=_("Your password must be at least 3 characters.")
    )
    password2 = CharField(
        label=_("Password Confirmation"),
        widget=PasswordInput,
        help_text=_("Please enter password again for confirmation.")
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2'
        ]

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self.instance:
            if self._meta.model.objects.filter(
                username=username
            ).exclude(pk=self.instance.pk).exists():
                raise ValidationError(
                    _("A user with this username already exists."),
                    code='username_exists',
                )
        else:
            if self._meta.model.objects.filter(
                username=username
            ).exists():
                raise ValidationError(
                    _("A user with this username already exists."),
                    code='username_exists',
                )
        return username
