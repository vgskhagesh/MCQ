from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class TestHome(TemplateView):
    template_name = "test_home.html"
