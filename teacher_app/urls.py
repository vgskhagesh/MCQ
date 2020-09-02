from django.urls import path
from django.contrib.auth import views as auth_views

from teacher_app.views import (TeacherHome, TeacherLogin, TeacherSignup, 
                                CreatePaper, ListPaper, DetailPaper, 
                                QuestionCreate, QuestionDetail, QuestionList,
                                PublishedListPaper
                                )

app_name = 'teacher_app'

urlpatterns = [
    path('',TeacherHome.as_view(),name='teacher_home'),
    path('login/',TeacherLogin.as_view(),name='teacher_login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='teacher_app:teacher_home'),name='teacher_logout'),
    path('signup/',TeacherSignup.as_view(),name='teacher_signup'),

    path('paper/new/',CreatePaper.as_view(),name="paper_form"),
    path('papers/',ListPaper.as_view(),name="paper_list"),
    path('papers/delete/<int:id>',ListPaper.as_view(),name="paper_list"),
    #path('papers/in/<slug:slug>/',DetailPaper.as_view(),name="paper_detail"),

    path('published/papers/',PublishedListPaper.as_view(),name="published_paper_list"),
    path('published/papers/<int:id>/',PublishedListPaper.as_view(),name="published_paper_list_approve"),

    path('questions/<slug:slug>/new/',QuestionCreate.as_view(),name="question_form"),
    path('questions/<slug:slug>/',QuestionList.as_view(),name="question_list"),
    path('questions/<slug:slug>/delete/<int:id>/',QuestionList.as_view(),name="question_list"),
    #path('question/<pk:pk>/',QuestionDetail.as_view(),name="question_detail"),
]
