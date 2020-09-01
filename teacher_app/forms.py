from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.db import transaction
from django import forms
from django.utils.translation import ugettext as _

from student_app.models import User
from teacher_app.models import Teacher

class TeacherLoginForm(AuthenticationForm):

    def confirm_login_allowed(self,user):
        if not user.is_teacher:
            raise forms.ValidationError(
                    _("Your account doesn't have access to Teacher. To proceed, please login with an account that has access."),
                    code='inactive',
                )

class TeacherSignupForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_teacher = True
        user.save()
        Teacher.objects.create(user=user)
        return user
