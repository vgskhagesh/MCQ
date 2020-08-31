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
    is_attempted = models.BooleanField(default=False)
    number = models.IntegerField(default=0)

    class AnswerChoices(models.TextChoices):
        A = 'A'
        B = 'B'
        C = 'C'
        D = 'D'
        E = 'E'
    answer = models.CharField(max_length=4,choices=AnswerChoices.choices,default=AnswerChoices.E)

    def is_upperclass(self):
        return self.answer in {
            self.AnswerChoices.A,
            self.AnswerChoices.B,
            self.AnswerChoices.C,
            self.AnswerChoices.D,
            self.AnswerChoices.E,
        }
    
    class Meta:
        ordering = ['number']