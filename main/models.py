from django.db import models
from shared.models import BaseModel
from django.core.validators import FileExtensionValidator
from shared.utility import validate_picture, validate_phone
from ckeditor.fields import RichTextField
from django.core.validators import MaxLengthValidator
from users.models import CustomUser

# Create your models here.
class Category(BaseModel):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, null=True, blank=True)


    def __str__(self):
        return self.name

class Tags(BaseModel):
    tag = models.CharField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        self.tag = self.tag.lower().strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.tag

class Post(BaseModel):
    picture = models.ImageField(upload_to="posts/", validators = [
        FileExtensionValidator(allowed_extensions=validate_picture)])
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    content = models.CharField(max_length=250)
    description = RichTextField()
    is_published = models.BooleanField(default=False)
    view_count = models.BigIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField(Tags, blank=True, related_name='posts')



    def __str__(self):
        return self.title

class About(BaseModel):
    full_name = models.CharField(max_length=250)
    picture = models.ImageField(upload_to="about/", validators=[
        FileExtensionValidator(allowed_extensions=validate_picture)])
    bio = models.TextField(validators=[MaxLengthValidator(5000)])

class Contact(BaseModel):
    name = models.CharField(max_length=250)
    phone = models.CharField(max_length=13, validators=[validate_phone])
    email = models.EmailField(max_length=250)
    message = models.TextField(validators=[MaxLengthValidator(5000)])

class Comment(models.Model):
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    message = RichTextField()

    is_public = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message