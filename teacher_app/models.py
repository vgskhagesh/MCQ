from django.db import models

from student_app.models import User

# Create your models here.

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)

class Paper(models.Model):
    title = models.CharField(max_length=100)
    def __str__(self):
        return self.title