# Generated by Django 3.0.6 on 2020-12-16 19:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teacher_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PaperClone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.IntegerField(default=0)),
                ('is_submitted', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now=True)),
                ('paper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paper_clone', to='teacher_app.Paper')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paper_clone_student', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-result'],
            },
        ),
        migrations.CreateModel(
            name='QuestionClone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_attempted', models.BooleanField(default=False)),
                ('number', models.IntegerField(default=0)),
                ('answer', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')], default='E', max_length=4)),
                ('paper_clone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_clone_paper_clone', to='test_app.PaperClone')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_clone', to='teacher_app.Question')),
            ],
            options={
                'ordering': ['number'],
            },
        ),
    ]
