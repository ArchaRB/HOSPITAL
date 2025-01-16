from django.db import models
from doctor.models import Doctor
# Create your models here.
class Patient(models.Model):
    name=models.TextField(max_length=50,null=True)
    email=models.TextField(max_length=50,null=True)
    password=models.TextField(max_length=50,null=True)
    otp=models.TextField(max_length=6,null=True)
    status=models.TextField(max_length=15,null=True)
    
class Appointment(models.Model):
    name=models.TextField(max_length=50,null=True)
    email=models.TextField(max_length=50,null=True)
    date=models.DateField(max_length=50,null=True)
    time=models.TimeField(max_length=50,null=True)
    message=models.TextField(max_length=500,null=True)
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    status=models.TextField(max_length=20)