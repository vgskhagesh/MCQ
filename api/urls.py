from django.urls import path, include
from .views import HelloView, CustomAuthToken

urlpatterns = [
    path("", HelloView.as_view(), name="hello"),
    path("token/", CustomAuthToken.as_view()),
]
