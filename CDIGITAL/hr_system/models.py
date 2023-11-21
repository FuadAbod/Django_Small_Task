from django.db import models

class UserProfile(models.Model):
    unique_identifier = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(null=True,blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    date_of_birth = models.DateField(null=True,blank=True)
    industry = models.CharField(null=True,blank=True,max_length=100)
    salary = models.DecimalField(null=True,blank=True,max_digits=10, decimal_places=2)
    years_of_experience = models.IntegerField(null=True,blank=True)


