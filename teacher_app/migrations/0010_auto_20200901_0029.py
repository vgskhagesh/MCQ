# Generated by Django 3.0.3 on 2020-08-31 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher_app', '0009_auto_20200901_0029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
