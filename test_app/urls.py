from django.urls import path

from .views import TestHome, TestQuestion, TestEnd, TestGenerateResult

app_name = "test_app"

urlpatterns = [
    path('<int:pk>/',TestHome.as_view(),name="test_home"),
    path('question/<int:pk>/',TestQuestion.as_view(),name="test_question"),
    path('end/',TestEnd.as_view(),name="test_end"),
    path('result/generate/',TestGenerateResult.as_view(),name="test_generate_result")
]