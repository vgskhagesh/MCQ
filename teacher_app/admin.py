from django.contrib import admin

from teacher_app.models import Teacher, Paper, Question
# Register your models here.

admin.site.register(Teacher)
admin.site.register(Paper)
admin.site.register(Question)