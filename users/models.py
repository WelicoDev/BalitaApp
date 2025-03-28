from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    profile_picture = models.ImageField(default="profile_default_picture.jpg", upload_to='profile_image')
    profession = models.CharField(max_length=250)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        super().save()