from django.contrib.auth.models import AbstractUser
from django.db import models



class Category(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 50, default = "")
    def __str__(self):
        return self.name

class User(AbstractUser):
    def __str__(self):
        return self.username
    pass


class Listing(models.Model):
    title = models.CharField(max_length = 100)
    start_bid = models.DecimalField(decimal_places=2, max_digits = 1000000)
    url = models.CharField(max_length = 200, blank = True)
    description = models.CharField(max_length = 200, default = "")
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = "category_listing", default  = "")
    watched = models.ManyToManyField(User, related_name = "watchedby", blank = True)
    def __str__(self):
        return f"{self.title} starting at ${self.start_bid}."


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "same_start_bid", default = "")
    current_bid = models.DecimalField(default = 0.00, decimal_places = 2, max_digits=100000)
    bidder = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    def __str__(self):
        return f"Current bid on {self.listing.title} is ${self.current_bid} by {self.bidder}"
    pass



    
class Comment(models.Model):
    pass 