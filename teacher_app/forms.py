from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.db import transaction
from django import forms
from django.utils.translation import ugettext as _

from student_app.models import User
from teacher_app.models import Teacher

class TeacherLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    password = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Password','type':'password'}))

    def confirm_login_allowed(self,user):
        if not user.is_teacher:
            raise forms.ValidationError(
                    _("Your account doesn't have access to Teacher. To proceed, please login with an account that has access."),
                    code='inactive',
                )

class TeacherSignupForm(UserCreationForm):
    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    first_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}))
    last_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}))
    password1 = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Password','type':'password'}))
    password2 = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Confirm Password','type':'password'}))

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_teacher = True
        user.save()
        Teacher.objects.create(user=user)
        return user
