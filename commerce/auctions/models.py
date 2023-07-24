from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.URLField(blank=False)
    price = models.DecimalField(decimal_places=2, max_digits=30)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    watched_at = models.ManyToManyField(User, blank=True, related_name="watchlist")
    winner = models.ForeignKey(User, null=True, related_name="winner", on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.DecimalField(decimal_places=2, max_digits=30)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder}"
    



class Comment(models.Model):
    commentor = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(blank=False)
    date = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.comment}"