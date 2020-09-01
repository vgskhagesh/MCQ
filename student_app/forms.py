from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from django import forms
from django.utils.translation import ugettext as _

from student_app.models import Student, User

class StudentLoginForm(AuthenticationForm):

    def confirm_login_allowed(self,user):
        if not user.is_student:
            raise forms.ValidationError(
                    _("Your account doesn't have access to Student. To proceed, please login with an account that has access."),
                    code='inactive',
                )

class StudentSignupForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        Student.objects.create(user=user)
        return user
