from django.db import models

# Create your models here.
class SignUp(models.Model):
	us1=models.CharField(max_length=30)  
	pass1=models.CharField(max_length=30) 
	email=models.CharField(max_length=30)
	mobile=models.CharField(max_length=30) 