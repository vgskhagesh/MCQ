from django.db import models

from teacher_app.models import Paper, Question

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.

class PaperClone(models.Model):
    paper = models.ForeignKey(Paper,on_delete=models.CASCADE,related_name="paper_clone")
    student = models.ForeignKey(User,on_delete=models.CASCADE,related_name="paper_clone_student")
    result = models.IntegerField(default=0)
    is_submitted = models.BooleanField(default=False)

class QuestionClone(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name="question_clone")
    paper_clone = models.ForeignKey(PaperClone,on_delete=models.CASCADE,related_name="question_clone_paper_clone")
    answer = models.CharField(max_length=10)
