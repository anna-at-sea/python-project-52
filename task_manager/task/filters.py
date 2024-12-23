import django_filters
from django.utils.translation import gettext_lazy as _

from task_manager.label.models import Label
from task_manager.status.models import Status
from task_manager.task.models import Task
from task_manager.user.models import User


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label=_("Status")
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label=_("Executor")
    )
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_("Label")
    )
    created_by_me = django_filters.BooleanFilter(
        method='filter_created_by_me',
        label=_("Show only my tasks"),
        widget=django_filters.widgets.forms.CheckboxInput()
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']

    def filter_created_by_me(self, queryset, name, value):
        if value:
            return queryset.filter(creator=self.request.user)
        return queryset
