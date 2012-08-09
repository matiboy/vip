from django.db import models
import django.contrib.auth.models

# Create your models here.
class Student(models.Model):
    user = models.ForeignKey(django.contrib.auth.models.User)