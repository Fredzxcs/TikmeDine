# Generated by Django 5.1.2 on 2024-10-22 06:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='security_question_1',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='security_question_2',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='security_question_3',
        ),
    ]
