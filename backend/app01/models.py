from django.db import models


# Create your models here.
class test(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    address = models.CharField(blank=True, max_length=20)
