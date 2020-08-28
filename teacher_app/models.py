from django.db import models
from django.utils.text import slugify
from django.urls import reverse

from student_app.models import User

from django import template
register = template.Library()

# Create your models here.

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)

class Paper(models.Model):
    name = models.CharField(max_length=100,default="")
    slug = models.SlugField(allow_unicode=True, unique=True,null=True)
    user = models.ForeignKey(User,related_name="paper",null=True,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        print("save")
        self.slug = slugify(self.name)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse("teacher_app:paper_detail", kwargs={"slug": self.slug})
    
    

class Question(models.Model):
    paper = models.ForeignKey(Paper,related_name="question",on_delete=models.CASCADE)

    def __str__(self):
        return paper.user.username