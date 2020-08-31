from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.http import Http404

from django.contrib.auth import get_user_model
User = get_user_model()

from teacher_app.models import Paper, Question
from .models import PaperClone, QuestionClone
from student_app.decorators import student_required

decorators = [login_required(login_url='student_app:student_login'),student_required()]

# Create your views here.

@method_decorator(decorators, name='dispatch')
class TestHome(DetailView):
    template_name = "test_home.html"
    model = Paper
    queryset = Paper
    
    def get_queryset(self):
        try:
            self.paper = Paper.objects.select_related("user").get(id__iexact=self.kwargs.get("pk"))
            self.paper_clone = PaperClone.objects.create(paper=self.paper,student=self.request.user)
            self.request.session["paper_id"] = self.kwargs.get("pk")
            self.request.session["paper_clone_id"] = self.paper_clone.id
            count = 0
            for _ in self.paper.question.all():
                count+=1
                QuestionClone.objects.create(question=_,paper_clone=self.paper_clone,number=count)
            self.request.session["question_count"] = count
        except:
            raise Http404
        else:
            return Paper.objects.filter(id=self.kwargs.get("pk"))

@method_decorator(decorators, name='dispatch')
class TestQuestion(UpdateView):
    template_name = "test_question.html"
    model = QuestionClone
    fields = ['answer']

    def get_context_data(self, **kwargs):
        try:
            self.question_clone = QuestionClone.objects.filter(paper_clone_id=self.request.session["paper_clone_id"]).get(number=self.kwargs.get("pk"))
            context = super().get_context_data(**kwargs)
            context["question"] = Question.objects.get(id=self.question_clone.question_id)
            context["question_number"] = self.question_clone.number

            context["sidebar_list"] = PaperClone.objects.get(id=self.request.session["paper_clone_id"]).question_clone_paper_clone.all()
        except:
            raise Http404
        else:
            return context

    def get_initial(self):
        try:
            self.question_clone = QuestionClone.objects.filter(paper_clone_id=self.request.session["paper_clone_id"]).get(number=self.kwargs.get("pk"))
        except:
            raise Http404
        else:
            return self.initial.copy()

    def form_valid(self,form):
        self.object = form.save(commit=False)
        if self.object.answer!="E":
            self.question_clone.answer = self.object.answer
            self.question_clone.is_attempted = True
            self.question_clone.save()
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.session["question_count"]<=self.question_clone.number:
            return reverse("test_app:test_end")
        return reverse("test_app:test_question", kwargs={"pk": self.question_clone.number+1})


@method_decorator(decorators, name='dispatch')
class TestEnd(TemplateView):
    template_name = "test_end.html"

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context["sidebar_list"] = PaperClone.objects.get(id=self.request.session["paper_clone_id"]).question_clone_paper_clone.all()
        except:
            raise Http404
        else:
            return context

@method_decorator(decorators, name='dispatch')
class TestGenerateResult(TemplateView):
    template_name = "test_generate_result.html"

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            self.paper_clone = PaperClone.objects.select_related("paper").get(id=self.request.session["paper_clone_id"])
            self.question_clone = self.paper_clone.question_clone_paper_clone.all()
            result = 0
            count = 0
            for _ in self.question_clone:
                count+=1
                if  Question.objects.get(id=_.question_id).key==_.answer:
                    result+=1
            context["percentage"] = result/count*100
            self.paper_clone.is_submitted = True
            self.paper_clone.result = result/count*100

            del self.request.session["paper_id"]
            del self.request.session["paper_clone_id"]
            del self.request.session["question_count"]
        except:
            raise Http404
        else:
            return context












