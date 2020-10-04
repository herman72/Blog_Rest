from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_time = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    author_comment = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_time = models.DateTimeField(default=timezone.now)

    post = models.ForeignKey('BlogApi.Post', on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.text


class UserBlog(AbstractUser):
    forget_password_code = models.CharField(max_length=32, null=True, blank=True)
    forget_password_code_expiration = models.DateTimeField(null=True, blank=True)
    following = models.ManyToManyField('UserBlog', related_name='followers')


