from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.shortcuts import redirect
from django.contrib.auth import login
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, CreateView, ListView, DetailView

from student_app.models import Student, User
from teacher_app.models import Paper, Question
from student_app.forms import StudentSignupForm, StudentLoginForm
from student_app.decorators import student_required

decorators = [login_required(login_url='student_app:student_login'),student_required()]
# Create your views here.

#@method_decorator([login_required(login_url='student_app:student_login'),student_required(login_url='student_app:student_login',redirect_field_name='student_app:student_home')], name='dispatch')
class StudentHome(TemplateView):
    template_name = 'student_home.html'

class ListPaper(ListView):
    model = Paper
    template_name = "paper_list.html"

class StudentLogin(LoginView):
    template_name = 'student_login.html'
    authentication_form = StudentLoginForm

    def get_success_url(self):
        url = self.get_redirect_url()
        if url:
            return url
        return reverse('student_app:student_home')

class StudentSignup(CreateView):
    template_name = 'student_signup.html'
    model = User
    form_class = StudentSignupForm
    success_url = reverse_lazy('')

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request,user)
        return redirect('student_app:student_home')

