from django.contrib.auth.models import AbstractUser
from django.db import models



class Category(models.Model):
    name = models.CharField(max_length = 50, default = "")
    def __str__(self):
        return self.name
class Listing(models.Model):
    title = models.CharField(max_length = 100)
    start_bid = models.IntegerField()
    url = models.CharField(max_length = 200, blank = True)
    description = models.CharField(max_length = 200, default = "")
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = "category_listing", default  = "")
    def __str__(self):
        return f"{self.title} starting at ${self.start_bid}."
class User(AbstractUser):
    watching = models.ManyToManyField(Listing, blank=True, related_name = "WatchedBy")
    
    pass

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "same_start_bid", default = "")
    current_bid = models.DecimalField(default = 0.00, decimal_places = 2, max_digits=100000)
    def __str__(self):
        return f"Current bid on {self.listing.title} is ${self.current_bid}"
    pass



    
class Comment(models.Model):
    pass 