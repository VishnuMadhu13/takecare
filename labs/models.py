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
    labname = models.CharField(max_length=150)

class labtestcat(models.Model):
    category = models.CharField(max_length=150)



class labtest(models.Model):
    category_id = models.CharField(max_length=150)
    name= models.CharField(max_length=150)
    amount = models.CharField(max_length=150)
    count = models.CharField(max_length=150)




class testreport(models.Model):
    p_id = models.CharField(max_length=150)
    height= models.CharField(max_length=150)
    weight = models.CharField(max_length=150)
    age = models.CharField(max_length=150)
    test1 = models.CharField(max_length=150)
    test2 = models.CharField(max_length=150)
    test3 = models.CharField(max_length=150)
    other = models.CharField(max_length=150)
