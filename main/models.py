from django.db import models

class Car_any(models.Model):
    url = models.CharField(max_length=255, primary_key=True)
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    photo = models.CharField(max_length=255)
    price = models.IntegerField()
    kms = models.IntegerField()
    contact = models.CharField(max_length=255, null=True)
    year = models.IntegerField(null=True)
    location = models.CharField(max_length=255, null=True)
    regSpecs = models.CharField(max_length=255, null=True)
    activeListings = models.IntegerField(null=True)
    posted = models.CharField(max_length=25, null=True)
    site = models.CharField(max_length=25, null=True)
    active = models.BooleanField(default=True)
    old_price = models.CharField(null=True, max_length=255)
    listing_type = models.CharField(max_length=255, null=True)
    listing_type_changed = models.BooleanField(default=False)
    notified = models.BooleanField(default=False)
    category_id_dubizzle = models.TextField(null=True)

class Brands(models.Model):
    name = models.CharField(max_length=25, unique=True)

class regSpecs(models.Model):
    name = models.CharField(max_length=127, unique=True)
    sites = []
    site = models.CharField(max_length=127, null=True)

class Listers(models.Model):
    id = models.CharField(max_length=127, unique=True, primary_key=True)