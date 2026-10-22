from django.db import models

# Create your models here.
from django.db import models
from django import forms

# Create your models here.
class admin(models.Model):
    email = models.CharField(max_length=150)
    password = models.CharField(max_length=150)

class time(models.Model):
    name = models.CharField(max_length=150)
    specialisation = models.CharField(max_length=150)
    date = models.CharField(max_length=150)
    start = models.CharField(max_length=150)
    end = models.CharField(max_length=150)
    status = models.CharField(max_length=150)
class homenurses(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
    specialisation = models.CharField(max_length=150)
    experience = models.CharField(max_length=150)
    amount = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    status = models.CharField(max_length=150)
