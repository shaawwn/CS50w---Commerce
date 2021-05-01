from django.contrib.auth.models import AbstractUser
from django.db import models

CATEGORIES = [

]
class User(AbstractUser):
    pass


class Category(models.Model):
    """Categories that listing items can be sorted into"""
    cat_type = models.CharField(max_length=16)


class Listing(models.Model):
    """Model for individual user created listing"""
    title = models.CharField(max_length=75)
    description = models.TextField(max_length=160)
    starting_bid = models.DecimalField(max_digits=999999, decimal_places=2)
    category = models.ManyToManyField(Category)
    seller = models.ForeignKey('User', default=None, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    image = models.ImageField(blank=True, null=True, upload_to="images/")
    

class Bid(models.Model):
    """Bids for a listing"""
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE)
    bid = models.FloatField()


class Comment(models.Model):
    """Comments on a listing"""
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE)
    comment = models.TextField(max_length=160)


