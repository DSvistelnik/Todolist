from django.contrib import admin
from goals.models import GoalCategory, Goal, GoalComment, Board


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user")


admin.site.register(GoalCategory, GoalCategoryAdmin)


class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'updated')
    search_fields = ('title', 'description')


admin.site.register(Goal, GoalAdmin)


class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'text',)
    readonly_fields = ('created', 'updated',)


admin.site.register(GoalComment, GoalCommentAdmin)


class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_deleted')
    readonly_fields = ('created', 'updated', )


admin.site.register(Board, BoardAdmin)