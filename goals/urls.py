from django.urls import path
from goals import views

urlpatterns = [
    #Доски
    path('board/create', views.BoardCreatedView.as_view(), name='create-board'),
    path('board/list', views.BoardListView.as_view(), name='board-list'),
    path('board/<int:pk>', views.BoardView.as_view(), name='board'),
    #Категории
    path("goal_category/create", views.GoalCategoryCreateView.as_view(), name='create-category'),
    path("goal_category/list", views.GoalCategoryListView.as_view(), name='category-list'),
    path("goal_category/<int:pk>", views.GoalCategoryView.as_view(), name='goal-category'),
    #Цели
    path("goal/create", views.GoalCreateView.as_view(), name='create-goal'),
    path("goal/list", views.GoalListView.as_view(), name='goal-list'),
    path("goal/<int:pk>", views.GoalView.as_view(), name='goal'),
    #Комментарии
    path("goal_comment/create", views.GoalCommentCreateView.as_view(), name='comment-create'),
    path("goal_comment/list", views.GoalCommentListView.as_view(), name='comment-list'),
    path("goal_comment/<int:pk>", views.GoalCommentView.as_view(), name='comment'),
]