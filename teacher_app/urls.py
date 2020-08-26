from django.urls import path
from django.contrib.auth import views as auth_views

from teacher_app.views import TeacherHome, TeacherLogin, TeacherSignup, TeacherPapers

app_name = 'teacher_app'

urlpatterns = [
    path('',TeacherHome.as_view(),name='teacher_home'),
    path('login/',TeacherLogin.as_view(),name='teacher_login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='teacher_app:teacher_home'),name='teacher_logout'),
    path('signup/',TeacherSignup.as_view(),name='teacher_signup'),
    path('papers/',TeacherPapers.as_view(),name='teacher_papers'),
]
