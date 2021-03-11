from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length = 50, default = "")
    def __str__(self):
        return f"{self.name} category"
class Listing(models.Model):
    title = models.CharField(max_length = 100)
    start_bid = models.IntegerField()
    url = models.CharField(max_length = 200, blank = True)
    description = models.CharField(max_length = 200, default = "")
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = "category_listing", default  = "")
    def __str__(self):
        return f"{self.title} starting at ${self.start_bid}."

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "same_start_bid", default = "")
    start_bid = models.ForeignKey(Listing, on_delete = models.CASCADE, default = 0)
    final_bid = models.IntegerField(default = 0)
    pass

class Comment(models.Model):
    pass 