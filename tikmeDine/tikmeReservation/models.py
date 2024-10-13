# models.py

from django.db import models

class DineInReservation(models.Model):
    date = models.DateField()
    total_books = models.IntegerField()

    def __str__(self):
        return f"Dine In on {self.date}"

class EventReservation(models.Model):
    date = models.DateField()
    total_books = models.IntegerField()

    def __str__(self):
        return f"Event on {self.date}"
