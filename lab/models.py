from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class labreg(models.Model):
    name = models.CharField(max_length=150)
    place = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    phno = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    status = models.CharField(max_length=150)


class labbill(models.Model):
    pid = models.CharField(max_length=150)
    medicine= models.CharField(max_length=150)
    date = models.CharField(max_length=150)
    rate = models.CharField(max_length=150)
    status = models.CharField(max_length=150)
