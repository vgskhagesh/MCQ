from django.urls import path
from django.contrib.auth import views as auth_views

from student_app.views import StudentHome, StudentLogin, StudentSignup, ListPaper

app_name = 'student_app'

urlpatterns = [
    path('',StudentHome.as_view(),name='student_home'),
    path('login/',StudentLogin.as_view(),name='student_login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='student_app:student_home'),name='student_logout'),
    path('signup/',StudentSignup.as_view(),name='student_signup'),

    path('papers/',ListPaper.as_view(),name="paper_list"),
]
