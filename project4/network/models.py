from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    people_followed = models.ManyToManyField('self',blank=True, related_name='follow')

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_content = models.TextField(blank=False)
    date = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(User, blank=True, related_name="like")
    def __str__(self):
        return f"{self.user}"
    def likes_count(self):
        return self.liked_by.count()

class Comment(models.Model):
    comment = models.TextField(blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.comment}"


