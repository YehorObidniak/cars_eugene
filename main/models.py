from django.db import models

# Create your models here.
class DubicarsCar(models.Model):
    url = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    photo = models.CharField(max_length=255)
    price = models.IntegerField()
    kms = models.IntegerField()
    phone = models.CharField(max_length=255, null=True)

class DubizzleCar(models.Model):
    url = models.CharField(max_length=255)
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    photo = models.CharField(max_length=255, null=True)
    price = models.IntegerField()
    kilometers = models.IntegerField()
    posted = models.CharField(max_length=25)
    active_listings_count = models.CharField(max_length=255)
    reg_specs = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

class YallamotorCar(models.Model):
    url = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    photo = models.CharField(max_length=255)
    price = models.IntegerField()
    kms = models.IntegerField()
    contact = models.CharField(max_length=15)
