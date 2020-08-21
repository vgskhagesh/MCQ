from django.http import HttpResponse
import datetime
from django.views.generic import TemplateView

class HomePage(TemplateView):
    template_name = 'home.html'