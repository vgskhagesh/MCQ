from django.http import request
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.shortcuts import redirect
from django.contrib.auth import login
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.http import Http404

from student_app.models import Student, User
from teacher_app.models import Paper, Question
from student_app.forms import StudentSignupForm, StudentLoginForm
from student_app.decorators import student_required
from test_app.models import PaperClone, QuestionClone

decorators = [login_required(login_url='student_app:student_login'),student_required()]
# Create your views here.

#@method_decorator([login_required(login_url='student_app:student_login'),student_required(login_url='student_app:student_login',redirect_field_name='student_app:student_home')], name='dispatch')
class StudentHome(TemplateView):
    template_name = 'student_home.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["paper_count"] = PaperClone.objects.filter(student=self.request.user).filter(is_submitted=True).count
        except :
            pass
        return context
    

class ListPaper(ListView):
    model = Paper
    template_name = "paper/paper_list.html"

class ListResult(ListView):
    template_name = "result_list_student.html"
    model = PaperClone

    def get_queryset(self):
        if self.kwargs.get("user_id"):
            self.paper_clone = PaperClone.objects.filter(student=self.kwargs.get("user_id")).filter(is_submitted=True)
        elif self.kwargs.get("paper_id"):
            self.paper_clone = PaperClone.objects.filter(paper=self.kwargs.get("paper_id")).filter(is_submitted=True)
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["paper_list"] = self.paper_clone
        context["student"] = True
        if self.kwargs.get("user_id"):
            context["student_user"] = User.objects.get(id=self.kwargs.get("user_id"))
        elif self.kwargs.get("paper_id"):
            context["student_paper"] = Paper.objects.get(id=self.kwargs.get("paper_id"))
        return context
    

class DetailUSer(DetailView):
    model = User
    template_name = "user_detail_student.html"


    def get_context_data(self, **kwargs):
        self.user_detail = User.objects.get(id=self.kwargs.get("pk"))
        context = super().get_context_data(**kwargs)
        context["user_detail"] = self.user_detail
        context["student_user_detail"] = True
        if self.request.user.is_authenticated:
            context["auth"] = True
        return context
    
    




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

