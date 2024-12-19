from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import UpdateView
from django.views.generic.edit import CreateView, DeleteView

from .forms import StatusForm
from .models import Status


class StatusIndexView(LoginRequiredMixin, View):

    def handle_no_permission(self):
        messages.error(self.request, _("You are not logged in! Please log in."))
        return redirect('login')

    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all()
        return render(request, 'pages/status/index.html', context={
            'statuses': statuses
        })


class StatusFormCreateView(LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'pages/status/create.html'
    success_url = reverse_lazy('status_index')

    def handle_no_permission(self):
        messages.error(self.request, _("You are not logged in! Please log in."))
        return redirect('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _("Status is created successfully"))
        return response


class StatusFormUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'pages/status/update.html'
    success_url = reverse_lazy('status_index')
    context_object_name = 'status'

    def handle_no_permission(self):
        messages.error(self.request, _("You are not logged in! Please log in."))
        return redirect('login')

    def form_valid(self, form):
        messages.success(self.request, _("Status is updated successfully"))
        return super().form_valid(form)


class StatusFormDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'pages/status/delete.html'
    success_url = reverse_lazy('status_index')
    context_object_name = 'status'

    def handle_no_permission(self):
        print("handle no permission called")
        messages.error(self.request, _("You are not logged in! Please log in."))
        return redirect('login')

    def form_valid(self, form):
        try:
            self.object.delete()
            messages.success(self.request, _("Status is deleted successfully"))
        except ProtectedError:
            messages.error(
                self.request, _("Cannot delete status while it is being used")
            )
        return redirect('status_index')
