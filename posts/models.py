from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.content

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    on_post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Comment, self).save(*args, **kwargs)

    def __str__(self):
        return self.content