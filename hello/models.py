from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)

class Banks(models.Model):
    id = models.BigIntegerField()	
    name = models.CharField(max_length=49)

    class Meta:
        db_table = "banks"


class BankBranches(models.Model):
    ifsc = models.CharField(max_length=11, primary_key=True)
    bank_id = models.BigIntegerField()
    branch = models.CharField(max_length=74)
    address = models.CharField(max_length=195)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=26)
    bank_name = models.CharField(max_length=49)   

    class Meta:    
        db_table = 'bank_branches'
