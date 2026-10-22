from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class pregister(models.Model):
    p_name = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    height=models.CharField(max_length=150)
    weight=models.CharField(max_length=150)
    pincode = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    age = models.CharField(max_length=150)
    status = models.CharField(max_length=150)

class booking(models.Model):
    pid = models.CharField(max_length=150)
    did = models.CharField(max_length=150)
    rate = models.CharField(max_length=150)

    date = models.CharField(max_length=150)
    status = models.CharField(max_length=150)


class medical_report(models.Model):
    patient_illness = models.CharField(max_length=150)
    test_report = models.CharField(max_length=150)
    height = models.CharField(max_length=150)
    weight = models.CharField(max_length=150)
    age = models.CharField(max_length=150)
    bloodgrp = models.CharField(max_length=150)
    gender = models.CharField(max_length=150)
    pid = models.CharField(max_length=150)
    file = models.CharField(max_length=150)


class requests(models.Model):
    dname= models.CharField(max_length=150)
    diseases = models.CharField(max_length=150)
    medicine = models.CharField(max_length=150)
    date = models.CharField(max_length=150)
    pharmacy = models.CharField(max_length=150)
    lab = models.CharField(max_length=150)
    pid = models.CharField(max_length=150)
    status = models.CharField(max_length=150)
class homenurserequest(models.Model):
    homenurse_id= models.CharField(max_length=150)
    description = models.CharField(max_length=150)
    amount = models.CharField(max_length=150)
    cardname=models.CharField(max_length=150)
    cardtype=models.CharField(max_length=150)
    cardno=models.CharField(max_length=150)
    status = models.CharField(max_length=150)
    pid = models.CharField(max_length=150)
    

class payment(models.Model):
    pid= models.CharField(max_length=150)
    pname=models.CharField(max_length=150)
    medicine = models.CharField(max_length=150)
    date = models.CharField(max_length=150)
    rate = models.CharField(max_length=150)
    cardno = models.CharField(max_length=150)
    cardname= models.CharField(max_length=150)
    cardmonth= models.CharField(max_length=150)
    cardyear= models.CharField(max_length=150)
    cv= models.CharField(max_length=150)


class d_payment(models.Model):
    pid= models.CharField(max_length=150)
    medicine = models.CharField(max_length=150)
    date = models.CharField(max_length=150)
    rate = models.CharField(max_length=150)
    cardno = models.CharField(max_length=150)
    cardname= models.CharField(max_length=150)
    cardmonth= models.CharField(max_length=150)
    cardyear= models.CharField(max_length=150)
    cv= models.CharField(max_length=150)
    dname= models.CharField(max_length=150)

class l_payment(models.Model):
    pid= models.CharField(max_length=150)
    medicine = models.CharField(max_length=150)
    date = models.CharField(max_length=150)
    rate = models.CharField(max_length=150)
    cardno = models.CharField(max_length=150)
    cardname= models.CharField(max_length=150)
    cardmonth= models.CharField(max_length=150)
    cardyear= models.CharField(max_length=150)
    cv= models.CharField(max_length=150)
    labname= models.CharField(max_length=150)
