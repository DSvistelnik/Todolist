from typing import Any
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.request import Request
from goals.models import Board, BoardParticipant, GoalCategory, Goal


class BoardPermissions(IsAuthenticated):

    def has_object_permission(self, request: Request, view, obj: Board) -> bool:
        _filters: dict[str: Any] = {'user_id': request.user.id, 'board_id': obj.id}
        if request.method not in SAFE_METHODS:
            _filters['role'] = BoardParticipant.Role.owner

        return BoardParticipant.objects.filter(**_filters).exists()


class GoalCategoryPermissions(IsAuthenticated):

    def has_object_permission(self, request: Request, view, goal_category: GoalCategory) -> bool:
        _filters: dict[str: Any] = {'user_id': request.user.id, 'board_id': goal_category.board_id}
        if request.method not in SAFE_METHODS:
            _filters['role'] = BoardParticipant.Role.owner

        return BoardParticipant.objects.filter(**_filters).exists()


class GoalBoardPermissions(IsAuthenticated):

    def has_object_permission(self, request: Request, view, obj: Goal) -> bool:
        _filters: dict[str: Any] = {'user': request.user.id, 'board': obj.category.board}
        if request.method not in SAFE_METHODS:
            _filters['role__in'] = [BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        return BoardParticipant.objects.filter(**_filters).exists()