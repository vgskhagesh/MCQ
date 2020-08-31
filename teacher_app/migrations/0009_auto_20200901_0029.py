# Generated by Django 3.0.3 on 2020-08-31 18:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher_app', '0008_auto_20200831_2130'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='paper',
            options={'ordering': ['-pub_date']},
        ),
        migrations.AlterField(
            model_name='paper',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 1, 0, 29, 14, 31414)),
        ),
    ]
