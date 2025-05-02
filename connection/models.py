from django.db import models

# Create your models here.
class Connection(models.Model):
    name= models.CharField(max_length=150,default='')
    host= models.CharField(default='localhost',max_length=150)
    port= models.IntegerField(default=3306)
    user= models.CharField(max_length=150,default='root')
    password= models.CharField(max_length=200,default='')
    database= models.CharField(max_length=150,default='')
    date_add = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)

