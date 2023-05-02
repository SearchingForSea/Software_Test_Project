from django.db import models

# Create your models here.
class test(models.Model):
    index = models.CharField(max_length=20)
    shard = models.IntegerField()
    prirep = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    docs = models.IntegerField()
    store = models.CharField(max_length=20)
    ip = models.CharField(max_length=20)
    node = models.CharField(max_length=20)
