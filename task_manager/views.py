# from django.shortcuts import render
from django.views.generic.base import TemplateView


# def index(request):
#     return render(request, 'index.html')


class IndexView(TemplateView):

    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
