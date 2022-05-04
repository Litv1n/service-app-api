from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from user.managers import UserManager


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

    def __str__(self):
        return f'{self.restaurant.name}, {self.menu_day}'
