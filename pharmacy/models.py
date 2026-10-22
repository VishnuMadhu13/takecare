from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

class phregister(models.Model):
    name = models.CharField(max_length=150)
    place = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    phno = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    status = models.CharField(max_length=150)

class bill(models.Model):
    pid = models.CharField(max_length=150)
    medicine = models.CharField(max_length=150)
    date = models.CharField(max_length=150)
    rate = models.CharField(max_length=150)
    status = models.CharField(max_length=150)
    pharmacyname = models.CharField(max_length=150)

class stock(models.Model):
    medicine = models.CharField(max_length=150)
    rate = models.CharField(max_length=150)
    export_date = models.CharField(max_length=150)
    expiry_date = models.CharField(max_length=150)
    availability = models.CharField(max_length=150)
