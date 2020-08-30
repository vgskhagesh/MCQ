from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.shortcuts import redirect
from django.contrib.auth import login
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from datetime import datetime

from django.contrib.auth import get_user_model
User = get_user_model()

#from student_app.models import User
from teacher_app.models import Teacher, Paper, Question
from teacher_app.forms import TeacherSignupForm, TeacherLoginForm
from teacher_app.decorators import teacher_required

decorators = [login_required(login_url='teacher_app:teacher_login'),teacher_required()]

# Create your views here.

@method_decorator(decorators, name='dispatch')
class TeacherHome(TemplateView):
    template_name = 'teacher_home.html'


@method_decorator(decorators, name='dispatch')
class CreatePaper(CreateView):
    template_name = 'paper_form.html'
    model = Paper
    fields = ('name','description')

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

@method_decorator(decorators, name='dispatch')
class QuestionCreate(CreateView):
    model = Question
    fields = ('question','option1','option2','option3','option4','key')
    template_name = "question_form.html"

    def get_initial(self):
        #print("QuestionCreate:",self.kwargs)
        if Paper.objects.select_related("user").get(slug__iexact=self.kwargs.get("slug")).is_published:
            raise Http404
        return self.initial.copy()

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.paper = Paper.objects.select_related("user").get(slug__iexact=self.kwargs.get("slug"))
        self.object.save()
        return super().form_valid(form)

@method_decorator(decorators, name='dispatch')
class PublishedListPaper(ListView):
    model = Paper
    template_name = "published_paper_list.html"

    def get_queryset(self):
        print(self.kwargs)
        try:
            self.cache = Paper.objects.select_related("user").get(id__iexact=self.kwargs.get("id"))
            if not self.cache.is_published:
                self.cache.is_published = True
                self.cache.pub_date = datetime.now()
                self.cache.save()
            print(cache)
        except:
            pass
        self.paper_user = Paper.objects.filter(user=self.request.user).filter(is_published=True)
        return self.paper_user

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['paper_user'] = self.paper_user
        return context

@method_decorator(decorators, name='dispatch')
class ListPaper(ListView):
    model = Paper
    template_name = "paper_list.html"

    def get_queryset(self):
        self.paper_user = Paper.objects.filter(user=self.request.user).filter(is_published=False)
        return self.paper_user

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['paper_user'] = self.paper_user
        return context

@method_decorator(decorators, name='dispatch')
class QuestionList(ListView):
    model = Question
    template_name = "question_list.html"

    def get_queryset(self):
        print(self.kwargs)
        try:
            print(Paper.objects.select_related("user").all())
            self.question_paper = Paper.objects.select_related("user").get(
                slug__iexact=self.kwargs.get("slug")
            )
            self.question_list = Question.objects.filter(paper=self.question_paper)
            print(self.question_paper)
        except User.DoesNotExist:
            raise Http404
        else:
            return self.question_paper.question.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question_paper"] = self.question_paper
        context["question_list"] = self.question_list
        return context

@method_decorator(decorators, name='dispatch')
class DetailPaper(DetailView):
    model = Paper
    template_name = "paper_detail.html"

@method_decorator(decorators, name='dispatch')
class QuestionDetail(DetailView):
    model = Question
    template_name = "question_detail.html"

    def get_queryset(self):
        query_set = super().get_queryset()
        return query_set.all()
        










class TeacherLogin(LoginView):
    template_name = 'teacher_login.html'
    authentication_form = TeacherLoginForm

    def get_success_url(self):
        url = self.get_redirect_url()
        if url:
            return url
        return reverse('teacher_app:teacher_home')

class TeacherSignup(CreateView):
    template_name = 'teacher_signup.html'
    model = User
    form_class = TeacherSignupForm
    success_url = reverse_lazy('')

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request,user)
        return redirect('teacher_app:teacher_home')

