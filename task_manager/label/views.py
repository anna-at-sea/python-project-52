from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import UpdateView
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView

from task_manager.label.forms import LabelForm
from task_manager.label.models import Label
from task_manager.utils import UserLoginRequiredMixin


class LabelIndexView(UserLoginRequiredMixin, ListView):
    model = Label
    template_name = 'pages/label/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['labels'] = Label.objects.all()
        return context


class LabelFormCreateView(
    UserLoginRequiredMixin, SuccessMessageMixin, CreateView
):
    model = Label
    form_class = LabelForm
    template_name = 'pages/label/create.html'
    success_url = reverse_lazy('label_index')
    success_message = _("Label is created successfully")


class LabelFormUpdateView(
    UserLoginRequiredMixin, SuccessMessageMixin, UpdateView
):
    model = Label
    form_class = LabelForm
    template_name = 'pages/label/update.html'
    success_url = reverse_lazy('label_index')
    context_object_name = 'label'
    success_message = _("Label is updated successfully")


class LabelFormDeleteView(
    UserLoginRequiredMixin, SuccessMessageMixin, DeleteView
):
    model = Label
    template_name = 'pages/label/delete.html'
    success_url = reverse_lazy('label_index')
    context_object_name = 'label'
    success_message = _("Label is deleted successfully")

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ValidationError:
            messages.error(
                self.request, _("Cannot delete label while it is being used")
            )
            return redirect('label_index')
