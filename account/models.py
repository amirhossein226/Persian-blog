from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from blog.models import Post
from .mytools import user_folder
# Create your models here.


class CustomUser(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    photo = models.ImageField(
        "عکس پروفایل",
        upload_to=user_folder,
        blank=True
    )
    archived_posts = models.ManyToManyField(
        Post, blank=True, related_name="archived_by")
    read_posts = models.ManyToManyField(
        Post, blank=True, related_name='read_by')

    def __str__(self):
        return self.user.username
