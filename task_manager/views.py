from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.utils.translation import gettext as _


class IndexView(TemplateView):

    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LoginView(View):

    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.add_message(
                request,
                messages.SUCCESS,
                _("You are logged in")
            )
            return redirect('index')
        return render(request, 'login.html', {'form': form})


class LogoutView(View):

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(
            request,
            messages.INFO,
            _("You are logged out")
        )
        return redirect('index')
