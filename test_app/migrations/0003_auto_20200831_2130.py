# Generated by Django 3.0.3 on 2020-08-31 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0002_auto_20200831_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionclone',
            name='answer',
            field=models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')], default='E', max_length=4),
        ),
    ]