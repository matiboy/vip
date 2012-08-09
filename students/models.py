from django.db import models
import django.contrib.auth.models

# Create your models here.
class Student(models.Model):
    user = models.ForeignKey(django.contrib.auth.models.User, primary_key=True)
    facebook_id = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    postcode = models.IntegerField( blank=True, null=True )
    city = models.CharField( max_length=255, blank=True, null=True )
    date_of_birth = models.DateField(blank=True, null=True)
    ic_number = models.CharField( max_length=255, blank=True, null=True )
