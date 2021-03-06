import uuid
import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from user.managers import UserManager


def menu_image_file_path(instance, filename):
    """Generate file path for new menu image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/menu/', filename)


class User(AbstractBaseUser, PermissionsMixin):
    """Create a custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Restaurant(models.Model):
    """Restaurant object"""
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    """Menu object"""
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE
    )
    MONDAY = 'M'
    TUESDAY = 'T'
    WEDNESDAY = 'W'
    THURSDAY = 'TH'
    FRIDAY = 'F'
    SATURDAY = 'S'
    SUNDAY = 'SU'
    DAY_OF_WEEK_CHOICES = [
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
        (SUNDAY, 'Sunday')
    ]
    menu_day = models.CharField(
        max_length=2,
        choices=DAY_OF_WEEK_CHOICES,
        default=MONDAY
    )
    image = models.ImageField(null=True, upload_to=menu_image_file_path)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.restaurant.name}, {self.menu_day}'


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.email} - {self.menu.restaurant.name}, {self.menu.menu_day}'
