"""mcq URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from mcq.views import HomePage
from student_app import urls as student_app_urls
from teacher_app import urls as teacher_app_urls
from test_app import urls as test_app_urls

urlpatterns = [
    path('',HomePage.as_view(),name='home'),
    path('admin/', admin.site.urls),
    path('student/',include(student_app_urls)),
    path('teacher/',include(teacher_app_urls)),
    path('test/',include(test_app_urls)),
]
