from django.db import models
from django.utils import timezone
from core.models import User


class BaseModel(models.Model):
    """Базовая модель"""
    created = models.DateField(
        verbose_name="Дата создания",
        null=True,
        blank=True,
    )
    updated = models.DateField(
        verbose_name="Дата последнего обновления",
        null=True,
        blank=True,
    )
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now().date()
        self.updated = timezone.now().date()

        return super().save(*args, **kwargs)


class Board(BaseModel):
    title = models.CharField(verbose_name='Название', max_length=255, blank=True)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)

    class Meta:
        verbose_name = "Доска"
        verbose_name_plural = "Доски"

    def __str__(self):
        return self.title


class BoardParticipant(Board):
    """Доски для пользователей"""
    class Meta:
        unique_together = ("board", "user")
        verbose_name = "Участник"
        verbose_name_plural = "Участники"

    class Role(models.IntegerChoices):
        owner = 1, "Владелец"
        writer = 2, "Редактор"
        reader = 3, "Читатель"

    board = models.ForeignKey(
        Board,
        verbose_name="Доска",
        on_delete=models.PROTECT,
        related_name="participants",
    )
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.PROTECT,
        related_name="participants",
    )
    role = models.PositiveSmallIntegerField(
        verbose_name="Роль", choices=Role.choices, default=Role.owner
    )
    editable_roles = Role.choices[1:]

    def __str__(self):
        return self.role


class GoalCategory(BaseModel):
    """Модель категории"""
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    board = models.ForeignKey(
        Board, verbose_name="Доска", on_delete=models.PROTECT, related_name="categories"
    )
    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)

    def __str__(self):
        return self.title


class Goal(BaseModel):
    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

    class Status(models.IntegerChoices):
        to_do = 1, 'К выполнению'
        in_progress = 2, 'В процессе'
        done = 3, 'Выполнено'
        archived = 4, 'Архив'

    class Priority(models.IntegerChoices):
        low = 1, 'Низкий'
        medium = 2, 'Средний'
        high = 3, 'Высокий'
        critical = 4, 'Критический'

    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        'goals.GoalCategory', on_delete=models.PROTECT, related_name='goals'
    )
    due_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey('core.User', on_delete=models.PROTECT)
    status = models.PositiveSmallIntegerField(
        choices=Status.choices, default=Status.to_do
    )
    priority = models.PositiveSmallIntegerField(
        choices=Priority.choices, default=Priority.medium
    )
    created = models.DateTimeField(verbose_name='Дата создания', auto_now=True)
    updated = models.DateTimeField(
        verbose_name='Дата последнего обновления', auto_now_add=True
    )

    def __str__(self) -> str:
        return self.title


class GoalComment(models.Model):
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    user = models.ForeignKey('core.User', on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='Дата создания', auto_now=True)
    updated = models.DateTimeField(
        verbose_name='Дата последнего обновления', auto_now_add=True
    )
    text = models.TextField()
    goal = models.ForeignKey('goals.Goal', on_delete=models.CASCADE)
