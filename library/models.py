from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Books(models.Model):
    ISBN_Code=models.CharField(max_length=50)
    Book_Title=models.CharField(max_length=200)
    Book_Author=models.CharField(max_length=200)
    Publication_year = models.IntegerField()
    Status=models.CharField(max_length=50, default="Available")
    Borrowed_By= models.CharField(max_length=200,default="")



class Details(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role_type = models.CharField(max_length=50)
    


