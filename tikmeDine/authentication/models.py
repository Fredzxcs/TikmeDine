from django.contrib.auth.models import AbstractUser
from django.db import models

class Employee(AbstractUser):
    ACCOUNT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('suspended', 'Suspended'),
    ]

    security_question_1 = models.CharField(max_length=255, blank=True, null=True)
    security_answer_1 = models.CharField(max_length=255, blank=True, null=True)
    security_question_2 = models.CharField(max_length=255, blank=True, null=True)
    security_answer_2 = models.CharField(max_length=255, blank=True, null=True)
    security_question_3 = models.CharField(max_length=255, blank=True, null=True)
    security_answer_3 = models.CharField(max_length=255, blank=True, null=True)
    account_setup_complete = models.BooleanField(default=False)
    account_status = models.CharField(
        max_length=50,
        choices=ACCOUNT_STATUS_CHOICES,
        default='pending',
    )
    role = models.CharField(
        max_length=50,
        choices=[('system_admin', 'System Admin'), ('employee', 'Employee')],
        default='employee',
    )

    job_title = models.CharField(max_length=255, blank=True, null=True)

    def is_system_admin(self):
        return self.role == 'system_admin'

    def is_employee(self):
        return self.role == 'employee'

    def __str__(self):
        return self.username
