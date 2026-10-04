from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    date_of_birth = models.DateField(null=True, blank=True)
    fav_author = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username