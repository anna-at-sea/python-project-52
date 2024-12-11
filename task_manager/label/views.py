from django.shortcuts import render, redirect
from django.views import View
from task_manager.label.models import Label
from django.core.exceptions import ValidationError
from task_manager.label.forms import LabelForm
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import LoginRequiredMixin


class LabelIndexView(LoginRequiredMixin, View):

    def handle_no_permission(self):
        messages.add_message(
            self.request,
            messages.ERROR,
            _("You are not logged in! Please log in.")
        )
        return redirect('login')

    def get(self, request, *args, **kwargs):
        labels = Label.objects.all()
        return render(request, 'label/index.html', context={
            'labels': labels
        })


class LabelFormCreateView(LoginRequiredMixin, View):

    def handle_no_permission(self):
        messages.add_message(
            self.request,
            messages.ERROR,
            _("You are not logged in! Please log in.")
        )
        return redirect('login')

    def get(self, request, *args, **kwargs):
        form = LabelForm()
        return render(request, 'label/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = LabelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                _("Label is created successfully")
            )
            return redirect('label_index')
        return render(request, 'label/create.html', {'form': form})


class LabelFormUpdateView(LoginRequiredMixin, View):

    def handle_no_permission(self):
        messages.add_message(
            self.request,
            messages.ERROR,
            _("You are not logged in! Please log in.")
        )
        return redirect('login')

    def get(self, request, *args, **kwargs):
        label_id = kwargs.get('id')
        label = Label.objects.get(id=label_id)
        form = LabelForm(instance=label)
        return render(
            request,
            'label/update.html',
            {'form': form, 'label_id': label_id}
        )

    def post(self, request, *args, **kwargs):
        label_id = kwargs.get('id')
        label = Label.objects.get(id=label_id)
        form = LabelForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                _("Label is updated successfully")
            )
            return redirect('label_index')
        return render(
            request,
            'label/update.html',
            {'form': form, 'label_id': label_id}
        )


class LabelFormDeleteView(LoginRequiredMixin, View):

    def handle_no_permission(self):
        messages.add_message(
            self.request,
            messages.ERROR,
            _("You are not logged in! Please log in.")
        )
        return redirect('login')

    def get(self, request, *args, **kwargs):
        label_id = kwargs.get('id')
        label = Label.objects.get(id=label_id)
        return render(
            request,
            'label/delete.html',
            {'label': label}
        )

    def post(self, request, *args, **kwargs):
        label_id = kwargs.get('id')
        label = Label.objects.get(id=label_id)
        if label:
            try:
                label.delete()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    _("Label is deleted successfully"))
            except ValidationError:
                messages.add_message(
                    request,
                    messages.ERROR,
                    _("Cannot delete label while it is being used"))
        return redirect('label_index')
