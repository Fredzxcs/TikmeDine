# Generated by Django 5.1.2 on 2024-10-24 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_remove_employee_security_question_1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='job_title',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
