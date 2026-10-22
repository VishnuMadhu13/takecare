from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class dregister(models.Model):
    name = models.CharField(max_length=150)
    specialisation = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    phno = models.CharField(max_length=150)
    fees = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    status = models.CharField(max_length=150)

class prescription(models.Model):
    pname = models.CharField(max_length=150)
    diseases = models.CharField(max_length=150)
    age = models.CharField(max_length=150)
    medicine1 = models.CharField(max_length=150)
    medicine2 = models.CharField(max_length=150)
    labtest = models.CharField(max_length=150)
    date = models.CharField(max_length=150)
    hname = models.CharField(max_length=150)

class vediocall(models.Model):
    pid = models.CharField(max_length=150)
    vedio = models.CharField(max_length=150)
    did = models.CharField(max_length=150)


