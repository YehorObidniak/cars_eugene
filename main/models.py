from django.db import models
from time import time

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
    listing_type_changed = models.IntegerField()
    notified = models.BooleanField(default=False)
    category_id_dubizzle = models.TextField(null=True)
    post_created_at = models.IntegerField(default=time())
    activeForSite = models.BooleanField(default=True)

class Brands(models.Model):
    name = models.CharField(max_length=25, primary_key=True)

class regSpecs(models.Model):
    name = models.CharField(max_length=127, unique=True)
    site = models.CharField(max_length=127, null=True)

class Sellers(models.Model):
    contact = models.CharField(max_length=255, primary_key=True)
    activeListings = models.IntegerField()
    site = models.CharField(max_length=255)