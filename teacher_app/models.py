from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from datetime import datetime
from django.utils.translation import gettext_lazy as _
import misaka

from student_app.models import User

from django import template
register = template.Library()

# Create your models here.

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)

class Paper(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,default="")
    slug = models.SlugField(allow_unicode=True, unique=True,null=True)
    user = models.ForeignKey(User,related_name="paper",null=True,on_delete=models.CASCADE)
    #date = models.DateTimeField(auto_now=True)
    date = models.DateTimeField(default=datetime.now())
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    pub_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        print("save")
        self.slug = slugify(self.id)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse("teacher_app:question_list", kwargs={"slug": self.slug})
    
    

class Question(models.Model):
    id = models.AutoField(primary_key=True)
    paper = models.ForeignKey(Paper,related_name="question",on_delete=models.CASCADE)
    question = models.TextField(blank=False,default="")
    option1 = models.CharField(max_length=100,blank=False,default="")
    option2 = models.CharField(max_length=100,blank=False,default="")
    option3 = models.CharField(max_length=100,blank=False,default="")
    option4 = models.CharField(max_length=100,blank=False,default="")
    date = models.DateTimeField(default=datetime.now())

    class AnswerChoices(models.TextChoices):
        A = 'A'
        B = 'B'
        C = 'C'
        D = 'D'
    key = models.CharField(max_length=4,choices=AnswerChoices.choices,default=AnswerChoices.A)

    def is_upperclass(self):
        return self.answer in {
            self.AnswerChoices.A,
            self.AnswerChoices.B,
            self.AnswerChoices.C,
            self.AnswerChoices.D,
        }

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.paper.user.username

    def save(self, *args, **kwargs):
        self.question = misaka.html(self.question)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("teacher_app:question_list", kwargs={"slug": self.paper.slug})