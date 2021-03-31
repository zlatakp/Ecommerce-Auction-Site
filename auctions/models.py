from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime



class Category(models.Model):
    id = models.AutoField(primary_key = True)
    url = models.CharField(default = "", max_length = 1000)
    name = models.CharField(max_length = 50, default = "")
    def __str__(self):
        return self.name

class User(AbstractUser):
    def __str__(self):
        return self.username
    pass


class Listing(models.Model):
    status_choice = [('active','active'), ('inactive','inactive')]
    winner = models.ForeignKey(User, on_delete = models.SET_DEFAULT, null = True, default = None, related_name = 'wonitems')
    
    status = models.CharField(max_length = 10, choices = status_choice, default = 'active')
    title = models.CharField(max_length = 100)
    start_bid = models.DecimalField(decimal_places=2, max_digits = 1000000)
    url = models.CharField(max_length = 200, blank = True)
    description = models.CharField(max_length = 200, default = "")
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = "category_listing", default  = "")
    watched = models.ManyToManyField(User, related_name = "watchedby", blank = True)
    owner = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True)
    def __str__(self):
        return f"{self.title} starting at ${self.start_bid} posted by {self.owner}."


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "same_start_bid", default = "")
    current_bid = models.DecimalField(default = 0.00, decimal_places = 2, max_digits=100000)
    bidder = models.ForeignKey(User, on_delete = models.SET_DEFAULT, null = True, default = None, blank = True, related_name = 'biddeditems')
    def __str__(self):
        return f"Current bid on {self.listing.title} is ${self.current_bid} by {self.bidder}"
    pass



    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, default = "")
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = 'comments', default = "")
    text = models.CharField(max_length=200, default = "")
    time = models.DateTimeField(default = datetime.now())
    def __str__(self):
        return f"{self.user} commented {self.text} at {self.time} on {self.listing.title} listing"
    pass 