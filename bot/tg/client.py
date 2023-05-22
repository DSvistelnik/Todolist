from django.conf import settings
from pydantic import ValidationError

from bot.tg.dc import GetUpdatesResponse, SendMessageResponse
from requests import Response
import requests


class TgClient:
    """Класс работы с телеграмм-ботом"""

    def __init__(self, token: str = settings.BOT_TOKEN) -> None:
        self.token = token

    def get_url(self, method: str) -> str:
        """Получаем urls в зависимости от метода"""
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        """Запрос обновления телеграмм-бота"""
        response: Response = requests.get(
            self.get_url('getUpdates'), params={'offset': offset, 'timeout': timeout}
        )
        data = response.json()
        return GetUpdatesResponse(**data)

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        """Отправить сообщение телеграмм-боту"""
        response: Response = requests.get(
            self.get_url('sendMessage'), params={'chat_id': chat_id, 'text': text}
        )
        data = response.json()
        return SendMessageResponse(**data)



