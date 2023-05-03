from django.db import transaction
from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework import permissions
from rest_framework.pagination import LimitOffsetPagination
from goals.filters import GoalDateFilter
from goals.models import GoalCategory, Goal, GoalComment, BoardParticipant, Board
from goals.permissions import BoardPermissions
from goals.serializers import GoalCreateSerializer, GoalCategoryCreateSerializer, GoalCategoryListSerializer, \
    GoalSerializer, GoalCommentCreateSerializer, GoalCommentSerializer, BoardSerializer, \
    BoardCreateSerializer, BoardListSerializer
from rest_framework.filters import OrderingFilter

class GoalCategoryCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryListSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['title', 'created']
    ordering = ['title']
    search_fields = ['title']

    def get_queryset(self) -> QuerySet:
        return GoalCategory.objects.select_related('user').filter(
            user=self.request.user, is_deleted=False
        )


class GoalCategoryView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryListSerializer

    def get_queryset(self) -> QuerySet:
        return GoalCategory.objects.select_related('user').filter(
            user=self.request.user, is_deleted=False
        )

    def perform_destroy(self, instance: GoalCategory) -> None:
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted',))
            instance.goals.update(status=Goal.Status.archived)


class GoalCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCreateSerializer


class GoalListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = GoalDateFilter
    ordering_fields = ['title', 'created']
    ordering = ['title']
    search_fields = ['title', 'description']

    def get_queryset(self) -> QuerySet:
        return (
            Goal.objects.select_related('user')
            .filter(user=self.request.user, category__is_deleted=False)
            .exclude(status=Goal.Status.archived)
        )


class GoalView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalSerializer

    def get_queryset(self) -> QuerySet:
        return (
            Goal.objects.select_related('user')
            .filter(user=self.request.user, category__is_deleted=False)
            .exclude(status=Goal.Status.archived)
        )

    def perform_destroy(self, instance: Goal) -> None:
        instance.status = Goal.Status.archived
        instance.save(update_fields=('status',))


class GoalCommentCreateView(generics.CreateAPIView):
    serializer_class = GoalCommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class GoalCommentListView(generics.ListAPIView):
    serializer_class = GoalCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['goal']
    ordering_fields = ['created', 'updated']
    ordering = ['-created']

    def get_queryset(self) -> QuerySet:
        return (
            GoalComment.objects.select_related('user')
            .filter(user=self.request.user)
            .exclude(goal__status=Goal.Status.archived)
        )


class GoalCommentView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GoalCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['goal']
    ordering_fields = ['created', 'updated']
    ordering = ['-created']

    def get_queryset(self) -> QuerySet:
        return (
            GoalComment.objects.select_related('user')
            .filter(user=self.request.user)
            .exclude(goal__status=Goal.Status.archived)
        )


class BoardCreatedView(generics.CreateAPIView):
    serializer_class = BoardCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        BoardParticipant.objects.create(user=self.request.user, board=serializer.save())


class BoardListView(generics.ListAPIView):
    serializer_class = BoardListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering = ['title']

    def get_queryset(self):
        return Board.objects.filter(participants__user_id=self.request.user.id, is_deleted=False)


class BoardView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.prefetch_related('participants__user').filter(is_deleted=False)

    def perform_destroy(self, instance: Board) -> None:
        with transaction.atomic():
            Board.objects.filter(id=instance.id).update(is_deleted=True)
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(status=Goal.Status.archived)
