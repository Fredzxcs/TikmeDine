from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class Employee(AbstractUser):
    security_question_1 = models.CharField(max_length=255, blank=True, null=True)
    security_answer_1 = models.CharField(max_length=255, blank=True, null=True)
    security_question_2 = models.CharField(max_length=255, blank=True, null=True)
    security_answer_2 = models.CharField(max_length=255, blank=True, null=True)
    security_question_3 = models.CharField(max_length=255, blank=True, null=True)
    security_answer_3 = models.CharField(max_length=255, blank=True, null=True)
    
    groups = models.ManyToManyField(
        Group,
        related_name='employee_user_set',  # Add related_name here
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='employee_user_permissions_set',  # Add related_name here
        blank=True,
    )
