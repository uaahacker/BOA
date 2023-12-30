from django.db import models
from django.contrib.auth.models import User
import uuid


class AccDetail(models.Model):
    
    
    buser = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    user_cnic = models.CharField(max_length=15, null=False)
    user_mobile = models.CharField(max_length=12)
    # @classmethod
    def generate_10_uuid():
        
        return uuid.uuid4().int % (10 ** 10)
    user_account_number = models.CharField(max_length=10,default=generate_10_uuid, unique=True)
    user_city = models.CharField(max_length=30)
    user_address = models.TextField(max_length=200)
    
    def __str__(self) -> str:
        return self.user_cnic
    
class Deposit(models.Model):
    duser = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    usr_data = models.ForeignKey(AccDetail, null=True, on_delete=models.SET_NULL)
    userbalance = models.FloatField(max_length=30, default=0.00)
    
    # def __str__(self) -> str:
    #     return self.duser.name
    


    
