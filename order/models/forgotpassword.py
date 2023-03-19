from django.db import models
from order.models import Customer

class Profile(models.Model):
    user=models.OneToOneField(Customer,on_delete=models.CASCADE)
    forgot_password_token=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)


     
        

    def register(self):
        self.save()
        