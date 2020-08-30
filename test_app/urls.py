from django.urls import path

from .views import TestHome

app_name = "test_app"

urlpatterns = [
    path('',TestHome.as_view(),name="test_home")
]