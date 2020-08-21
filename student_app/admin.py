from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from student_app.models import User, Student

admin.site.register(User, UserAdmin)
admin.site.register(Student)