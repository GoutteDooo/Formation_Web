from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id":self.id,
            "user":self.user.username,
            "content":self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes
        }

class FollowModel(models.Model):
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return f"{self.follower} follows {self.following}"