from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from django import forms
from django.utils.translation import ugettext as _

from student_app.models import Student, User

class StudentLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    password = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Password','type':'password'}))

    def confirm_login_allowed(self,user):
        if not user.is_student:
            raise forms.ValidationError(
                    _("Your account doesn't have access to Student. To proceed, please login with an account that has access."),
                    code='inactive',
                )

class StudentSignupForm(UserCreationForm):
    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    first_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}))
    last_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}))
    password1 = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Password','type':'password'}))
    password2 = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Confirm Password','type':'password'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        Student.objects.create(user=user)
        return user
