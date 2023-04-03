from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create models users
class User(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(10), MaxValueValidator(100)])

    REQUIRED_FIELDS: list[str] = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

