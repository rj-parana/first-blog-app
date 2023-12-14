from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django_extensions.db.fields import AutoSlugField
from django.utils.safestring import mark_safe
from ckeditor.fields import RichTextField


class User(AbstractUser):
    email = models.EmailField(max_length=160, unique=True)
    mobile = models.CharField(max_length=180, null=True, unique=True)
    city = models.CharField(max_length=120, null=True)
    country = models.CharField(max_length=140, null=True)
    image = models.ImageField(upload_to='user_images/')

    def __str__(self):
        return self.email

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title', unique=True)
    text = RichTextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='featured_images/%Y/%m/%d')
    thumbnail = models.ImageField(upload_to='thumbnails/%Y/%m/%d')
    
    def save(self, *args, **kwargs):
        self.published_date = timezone.now()
        super().save(*args, **kwargs)

    def get_image(self):
        return self.image

    def __str__(self):
        return self.title

    @property
    def thumbnail_preview(self):
        if self.thumbnail:
            return mark_safe('<img src="{}" width="100" height="80" />'.format(self.thumbnail.url))
        return ""

    @property
    def image_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="200" height="80" />'.format(self.image.url))
        return ""

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent= models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=80)
    content = models.TextField(max_length=500)
    active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.active = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)

class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='reply')
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=80)
    content = models.TextField(max_length=500)
    active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.active = True
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


