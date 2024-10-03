from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.conf import settings
from taggit.models import Tag
from .mytools import create_image_path
from django.urls import reverse

from tinymce.models import HTMLField
# Create your models here.


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

    class Status(models.TextChoices):
        PUBLISHED = ('PB', "منتشر شده")
        DRAFT = ("DF", "در انتظار تایید")

    title = models.CharField("عنوان", max_length=255)

    slug = models.SlugField(
        max_length=255,
        unique_for_date='publish',
        allow_unicode=True,
        blank=True
    )

    description = models.TextField("توضیح مختصر")

    body = HTMLField('متن کامل')

    authors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="posts"
    )

    created = models.DateTimeField(auto_now_add=True)
    publish = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT
    )

    tags = TaggableManager("تگ ها")

    photo = models.ImageField(
        upload_to=create_image_path,
        null=True,
        blank=True,
    )
    likes_count = models.PositiveIntegerField(default=0)
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='posts_liked',
        blank=True
    )
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):

        return reverse("blog:post_details", args=[
            self.publish.year,
            self.publish.month,
            self.publish.day,
            self.slug
        ])

    def generate_html_id(self):
        id = self.id * 10 - self.id * 3
        return id

    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.title):
            self.slug = slugify(self.title, allow_unicode=True)

        super().save(*args, **kwargs)


class Comment(models.Model):
    text = models.TextField("متن")
    author = models.CharField("نام", max_length=40)
    email = models.EmailField("آدرس ایمیل")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE,
        related_name='comments'
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return f"Wrote By {self.author} for {self.post}"
