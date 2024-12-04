from django.shortcuts import render, redirect
from django.views import View
from task_manager.status.models import Status
from django.db.models import ProtectedError
from task_manager.status.forms import StatusForm
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import LoginRequiredMixin


class StatusIndexView(LoginRequiredMixin, View):

    def handle_no_permission(self):
        messages.add_message(
            self.request,
            messages.ERROR,
            _("You are not logged in! Please log in.")
        )
        return redirect('login')

    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all()
        return render(request, 'status/index.html', context={
            'statuses': statuses
        })


class StatusFormCreateView(LoginRequiredMixin, View):

    def handle_no_permission(self):
        messages.add_message(
            self.request,
            messages.ERROR,
            _("You are not logged in! Please log in.")
        )
        return redirect('login')

    def get(self, request, *args, **kwargs):
        form = StatusForm()
        return render(request, 'status/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                _("Status is created successfully")
            )
            return redirect('status_index')
        return render(request, 'status/create.html', {'form': form})


class StatusFormUpdateView(LoginRequiredMixin, View):

    def handle_no_permission(self):
        messages.add_message(
            self.request,
            messages.ERROR,
            _("You are not logged in! Please log in.")
        )
        return redirect('login')

    def get(self, request, *args, **kwargs):
        status_id = kwargs.get('id')
        status = Status.objects.get(id=status_id)
        form = StatusForm(instance=status)
        return render(
            request,
            'status/update.html',
            {'form': form, 'status_id': status_id}
        )

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get('id')
        status = Status.objects.get(id=status_id)
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                _("Status is updated successfully")
            )
            return redirect('status_index')
        return render(
            request,
            'status/update.html',
            {'form': form, 'status_id': status_id}
        )


class StatusFormDeleteView(LoginRequiredMixin, View):

    def handle_no_permission(self):
        messages.add_message(
            self.request,
            messages.ERROR,
            _("You are not logged in! Please log in.")
        )
        return redirect('login')

    def get(self, request, *args, **kwargs):
        status_id = kwargs.get('id')
        status = Status.objects.get(id=status_id)
        return render(
            request,
            'status/delete.html',
            {'status': status}
        )

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get('id')
        status = Status.objects.get(id=status_id)
        if status:
            try:
                status.delete()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    _("Status is deleted successfully"))
            except ProtectedError:
                messages.add_message(
                    request,
                    messages.ERROR,
                    _("Cannot delete status while it is being used"))
        return redirect('status_index')
