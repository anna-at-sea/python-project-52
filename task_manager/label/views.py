from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from task_manager.label.forms import LabelForm
from task_manager.label.models import Label
from task_manager.utils import (
    CreateViewMixin, DeleteViewMixin, UpdateViewMixin, UserLoginRequiredMixin
)


class LabelIndexView(UserLoginRequiredMixin, ListView):
    model = Label
    template_name = 'pages/index_label.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['labels'] = Label.objects.all()
        return context


class LabelFormCreateView(
    CreateViewMixin, UserLoginRequiredMixin, SuccessMessageMixin, CreateView
):
    model = Label
    form_class = LabelForm


class LabelFormUpdateView(
    UpdateViewMixin, UserLoginRequiredMixin, SuccessMessageMixin, UpdateView
):
    model = Label
    form_class = LabelForm


class LabelFormDeleteView(
    DeleteViewMixin, UserLoginRequiredMixin, SuccessMessageMixin, DeleteView
):
    model = Label
