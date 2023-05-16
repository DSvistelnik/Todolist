import os
from django.db import models
from core.models import User
from django.utils.crypto import get_random_string


class TgUser(models.Model):
    """Модель пользователя бота"""
    chat_id = models.BigIntegerField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    verification_code = models.CharField(max_length=50, null=True, blank=True, default=None)

    @staticmethod
    def generate_verification_code() -> str:
        """
        Генерация верификационного кода
        """
        return get_random_string(length=50)
