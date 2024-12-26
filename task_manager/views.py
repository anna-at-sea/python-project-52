from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'layouts/form_base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'heading': _("Log in"),
            'button_text': _("Sign in")
        })
        return context

    def get_success_url(self):
        return reverse_lazy('index')

    def get_success_message(self, *args, **kwargs):
        return _("You are logged in")


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        messages.add_message(
            request,
            messages.INFO,
            _("You are logged out")
        )
        return super().dispatch(request, *args, **kwargs)
