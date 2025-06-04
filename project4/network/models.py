from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post:
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    