from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

def teacher_required(function=None, redirect_field_name='teacher_app:teacher_home', login_url='teacher_app:teacher_login'):
    actual_decorator = user_passes_test(
        lambda u : u.is_active and u.is_teacher,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator