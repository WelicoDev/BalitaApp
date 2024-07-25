from django.db import models
from shared.models import BaseModel
from ckeditor.fields import RichTextField

# Create your models here.

class Category(BaseModel):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)

    def __str__(self):
        return self.name

class Post(BaseModel):
    category = models.ForeignKey(Category , on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/')
    title = models.CharField(max_length=250)
    content = RichTextField()

    is_published = models.BooleanField(default=True)
    view_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title
