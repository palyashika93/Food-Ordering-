from django.db import models

class Feature(models.Model):
   
    title=models.CharField(max_length=100)
    body=models.CharField(max_length=100000)
    number=models.CharField(max_length=50)

class Special(models.Model):
    dishname=models.CharField(max_length=100)
    dishtitle=models.CharField(max_length=100000)
    dishdesc=models.CharField(max_length=1000000)

# Create your models here.
