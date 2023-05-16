from typing import Any
from django.core.management import BaseCommand
from django.db.models import QuerySet
from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message, GetUpdatesResponse, SendMessageResponse
from goals.models import Goal, GoalCategory


class Command(BaseCommand):
    """ Команды телеграмм-бота"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.tg_client: TgClient = TgClient()
        self.states: dict = {}

    def handle(self, *args: Any, **options: Any) -> None:
        offset: int = 0
        while True:
            res: GetUpdatesResponse = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(item.message)

    def handle_message(self, message: Message) -> None:
        """
        Обработка сообщений от авторизованного или неавторизованного пользователя
        """
        tg_user, created = TgUser.objects.get_or_create(chat_id=message.chat.id)

        if tg_user.user:
            self.handler_authorized_user(tg_user, message)
        else:
            self.handler_unauthorized_user(tg_user, message)

    def handler_authorized_user(self, tg_user: TgUser, message: Message) -> None:
        """
        Возвращение ответов пользователя
        """
        commands: list[str] = ['/goals', '/create', '/cancel']

        if not self.states.get('state') and message.text not in commands:
            self.tg_client.send_message(
                chat_id=message.chat.id, text=f'Unknown command!'
            )

        if message.text == '/cancel':
            self.states = {}
            self.tg_client.send_message(
                chat_id=message.chat.id, text='Operation was canceled'
            )

        if not self.states and message.text in commands:
            if message.text == '/goals':
                self._get_goals(message, tg_user)

            if message.text == '/create':
                self.states['state'] = 'creating'
                self._get_categories(message=message, tg_user=tg_user)

        if (
            self.states.get('state') == 'getting goal title'
            and message.text not in commands
        ):
            self.states['goal_title'] = message.text
            self._create_goal(
                chat_id=message.chat.id,
                title=self.states.get('goal_title'),
                user_id=tg_user.user.id,
                category_id=self.states.get('user_category_id'),
            )
            self.states = {}

        if self.states.get('state') == 'creating' and message.text not in commands:
            if message.text in self.states['categories_id']:
                self.tg_client.send_message(
                    chat_id=message.chat.id, text='Input goal title'
                )
                self.states['user_category_id'] = int(message.text)
                self.states['state'] = 'getting goal title'
            else:
                self.tg_client.send_message(
                    chat_id=message.chat.id, text='Wrong category!'
                )

    def handler_unauthorized_user(self, tg_user: TgUser, message: Message) -> None:
        """
        Верификация пользователя
        """
        verification_code: str = tg_user.generate_verification_code()
        tg_user.verification_code = verification_code
        tg_user.save()

        self.tg_client.send_message(
            chat_id=message.chat.id,
            text=f'Твой верификационный код {tg_user.verification_code}',
        )

    def _get_goals(self, message: Message, tg_user: TgUser) -> SendMessageResponse:
        """
        Возвращает пользователю информацию о целях
        """
        query_set: QuerySet = (
            Goal.objects.select_related('user')
            .filter(user_id=tg_user.user.id, category__is_deleted=False)
            .exclude(status=Goal.Status.archived)
        )
        goals = [f'{goal.id} {goal.title}' for goal in query_set]
        if not goals:
            text = 'No goals'
        else:
            text = '\n'.join(goals)
        return self.tg_client.send_message(chat_id=message.chat.id, text=text)

    def _get_categories(self, message: Message, tg_user: TgUser) -> SendMessageResponse:
        """
        Возвращает пользователю информацию о категориях
        """
        query_set: QuerySet = GoalCategory.objects.filter(
            board__participants__user=tg_user.user
        ).exclude(is_deleted=True)
        categories: list[str] = [
            f'{category.id} {category.title}' for category in query_set
        ]
        self.states['categories_id'] = [str(cat.id) for cat in query_set]
        if not categories:
            text: str = 'No categories'
        else:
            text = '\n'.join(categories)
        return self.tg_client.send_message(chat_id=message.chat.id, text=text)

    def _create_goal(
            self, chat_id: int, title: str | None, user_id: int, category_id: int | None
    ) -> SendMessageResponse:
        """
        Создание цели
        """
        Goal.objects.create(user_id=user_id, title=title, category_id=category_id)
        return self.tg_client.send_message(
            chat_id=chat_id, text=f'Goal {title} created!'
        )

