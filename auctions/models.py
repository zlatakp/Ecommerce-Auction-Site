from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length = 100)
    start_bid = models.IntegerField()
    url = models.CharField(max_length = 200, blank = True)
    description = models.CharField(max_length = 200, default = "")
    def __str__(self):
        return f"{self.title} starting at ${self.start_bid}."
class Category(models.Model):
    pass
class Bid(models.Model):
    pass

class Comment(models.Model):
    pass