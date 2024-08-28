from django.db import models
from shared.models import BaseModel
from ckeditor.fields import RichTextField

from users.models import CustomUser

class Tag(BaseModel):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

# Create your models here.

class Category(BaseModel):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)

    def __str__(self):
        return self.name

class Post(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category , on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/')
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    content = RichTextField()
    tag = models.ManyToManyField(Tag, blank=True)

    is_published = models.BooleanField(default=True)
    view_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Comment(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    message = models.TextField()

    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.message

class Contact(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=13)
    email = models.EmailField(max_length=128)
    message = models.TextField(null=True , blank=True)

    is_solved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name