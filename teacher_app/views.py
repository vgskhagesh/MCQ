from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.shortcuts import redirect
from django.contrib.auth import login
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from student_app.models import User
from teacher_app.models import Teacher, Paper
from teacher_app.forms import TeacherSignupForm, TeacherLoginForm, PaperForm
from teacher_app.decorators import teacher_required

# Create your views here.

@method_decorator([login_required(login_url='teacher_app:teacher_login'),teacher_required(login_url='teacher_app:teacher_login',redirect_field_name='teacher_app:teacher_home')], name='dispatch')
class TeacherHome(TemplateView):
    template_name = 'teacher_home.html'

class TeacherPapers(CreateView):
    template_name = 'teacher_papers.html'
    model = Paper
    form_class = PaperForm

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'paper'
        return super().get_context_data(**kwargs)

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.save()
        return super().form_valid(form)

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

