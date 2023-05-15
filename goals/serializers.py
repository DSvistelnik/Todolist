from datetime import datetime
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.db import transaction
from core.models import User
from core.serializers import ProfileSerializer
from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant


class BoardCreateSerializer(serializers.ModelSerializer):
    """ Создание доски"""
    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'is_deleted')


class BoardParticipantsSerializer(serializers.ModelSerializer):
    """Доска для пользователей"""
    role = serializers.ChoiceField(required=True, choices=BoardParticipant.editable_roles)

    user = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    board = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = BoardParticipant
        fields = "__all__"
        real_only_fields = (
            "id",
            "created",
            "updated",
            "board",
        )


class BoardSerializer(serializers.ModelSerializer):
    """ Работа с доской """
    participants = BoardParticipantsSerializer(many=True)

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = (
            "id",
            "created",
            "updated",
        )

    def update(self, instance: Board, validated_data) -> Board:
        user = self.context.get("request").user
        new_participants = {
            participant["user"].id: participant
            for participant in validated_data.pop("participants")
            if participant["user"] != user
        }

        old_participants = instance.participants.exclude(user=user)

        with transaction.atomic():
            for old_participant in old_participants:
                if old_participant.user.id not in new_participants:
                    old_participant.delete()

                else:
                    new_role = new_participants[old_participant.user.id]["role"]
                    if old_participant.role != new_role:
                        old_participant.role = new_role
                        old_participant.save()
                    del new_participants[old_participant.user.id]

            [
                BoardParticipant.objects.create(board=instance, **data)
                for data in new_participants.values()
            ]
            instance.title = validated_data.get("title")
            instance.save()

        return instance


class BoardListSerializer(serializers.ModelSerializer):
    """Отображение всех досок"""
    class Meta:
        model = Board
        fields = '__all__'


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    """Создание категории"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ('id', 'created', 'updated', 'user', 'is_deleted')
        fields = '__all__'


class GoalCategoryListSerializer(GoalCategoryCreateSerializer):
    """Сериалайзер для категории"""
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user", "is_deleted")
        fields = "__all__"


class GoalCreateSerializer(serializers.ModelSerializer):
    """Создание цели"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        read_only_fields = (
            'id',
            'created',
            'updated',
            'user',
        )
        fields = '__all__'

    def validate_category(self, value: GoalCategory) -> GoalCategory:
        if value.is_deleted:
            raise ValidationError('Category not found')

        if self.context['request'].user.id != value.user_id:
            raise PermissionDenied
        return value

    def validate_due_date(self, value: datetime) -> datetime:
        if value:
            if value < timezone.now().date():
                raise ValidationError('Date in the past')
            return value


class GoalSerializer(GoalCreateSerializer):
    """Сериалайзер для цели"""
    user = ProfileSerializer(read_only=True)


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    """Создание комментариев"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        read_only_fields = ['id', 'created', 'updated', 'user']
        fields = '__all__'

    def validate_goal(self, value: Goal) -> Goal:
        if value.status == Goal.Status.archived:
            raise ValidationError('Goal not found')

        if self.context['request'].user.id != value.user_id:
            raise PermissionDenied
        return value


class GoalCommentSerializer(GoalCommentCreateSerializer):
    """Сериалайзер для комментариев"""
    user = ProfileSerializer(read_only=True)
    goal = serializers.PrimaryKeyRelatedField(read_only=True)


