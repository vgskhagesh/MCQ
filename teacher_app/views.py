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

from django.contrib.auth import get_user_model
User = get_user_model()

#from student_app.models import User
from teacher_app.models import Teacher, Paper
from teacher_app.forms import TeacherSignupForm, TeacherLoginForm
from teacher_app.decorators import teacher_required

# Create your views here.

decorators = [login_required(login_url='teacher_app:teacher_login'),teacher_required()]

@method_decorator(decorators, name='dispatch')
class TeacherHome(TemplateView):
    template_name = 'teacher_home.html'


@method_decorator(decorators, name='dispatch')
class CreatePaper(CreateView):
    template_name = 'paper_form.html'
    model = Paper
    fields = ('name',)

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


@method_decorator(decorators, name='dispatch')
class ListPaper(ListView):
    model = Paper
    template_name = "paper_list.html"

    def get_queryset(self):
        self.paper_user = Paper.objects.filter(user=self.request.user)
        return self.paper_user

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['paper_user'] = self.paper_user
        return context


@method_decorator(decorators, name='dispatch')
class DetailPaper(DetailView):
    model = Paper
    template_name = "paper_detail.html"

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

