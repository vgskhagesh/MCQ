from django.contrib import admin

from test_app.models import PaperClone, QuestionClone

# Register your models here.

admin.site.register(PaperClone)
admin.site.register(QuestionClone)
