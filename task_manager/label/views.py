from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import UpdateView
from django.views.generic.edit import CreateView, DeleteView

from .forms import LabelForm
from .models import Label


class LabelIndexView(LoginRequiredMixin, View):

    def handle_no_permission(self):
        messages.error(self.request, _("You are not logged in! Please log in."))
        return redirect('login')

    def get(self, request, *args, **kwargs):
        labels = Label.objects.all()
        return render(request, 'label/index.html', context={
            'labels': labels
        })


class LabelFormCreateView(LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'label/create.html'
    success_url = reverse_lazy('label_index')

    def handle_no_permission(self):
        messages.error(self.request, _("You are not logged in! Please log in."))
        return redirect('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _("Label is created successfully"))
        return response


class LabelFormUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'label/update.html'
    success_url = reverse_lazy('label_index')
    context_object_name = 'label'

    def handle_no_permission(self):
        messages.error(self.request, _("You are not logged in! Please log in."))
        return redirect('login')

    def form_valid(self, form):
        messages.success(self.request, _("Label is updated successfully"))
        return super().form_valid(form)


class LabelFormDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'label/delete.html'
    success_url = reverse_lazy('label_index')
    context_object_name = 'label'

    def handle_no_permission(self):
        messages.error(self.request, _("You are not logged in! Please log in."))
        return redirect('login')

    def form_valid(self, form):
        try:
            self.object.delete()
            messages.success(self.request, _("Label is deleted successfully"))
        except ValidationError:
            messages.error(
                self.request, _("Cannot delete label while it is being used")
            )
        return redirect('label_index')
