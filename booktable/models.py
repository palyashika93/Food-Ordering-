from django.db import models
from django.db.models.fields import Field

# Create your models here.
class Table_booked(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.IntegerField()
    date=models.DateField()
    time=models.TimeField()
    no_of_persons=models.IntegerField()
    message=models.TextField(null=True)
