# Generated by Django 3.0.3 on 2020-08-31 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0003_auto_20200831_2130'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='questionclone',
            options={'ordering': ['number']},
        ),
    ]