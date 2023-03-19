from django.db import models
from django.db.models.fields import CharField

class Customer(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    password=models.CharField(max_length=500)
    password2=models.CharField(max_length=500)

    def register(self):
        self.save()

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False
    @staticmethod
    def get_customer_by_name(name):
        try:
            return Customer.objects.get(name=name)       
        except:
            return False
   


    def isExists(self):
        if Customer.objects.filter(email=self.email):
            return True
        return False

                 