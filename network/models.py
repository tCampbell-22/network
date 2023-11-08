from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField("self", symmetrical=False, related_name="followers")
    def follow_count(self):
        return f"{self.followers.all().count()} {'follower' if self.followers.all().count() == 1 else 'followers'}"

class Post(models.Model):
    author = models.ForeignKey("User", on_delete=models.CASCADE, blank=True)
    likes = models.ManyToManyField(User,  blank=True, related_name="liked_user")
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.author} | {self.timestamp} | {self.likes} likes:  {self.body}"
    def likes_count (self):
        return f"{self.likes.all().count()} {'like' if self.likes.all().count() == 1 else 'likes'}"
    
