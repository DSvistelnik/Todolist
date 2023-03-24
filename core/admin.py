from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('email', 'first_name', 'last_name', 'username')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    readonly_fields = ('last_login', 'date_joined')

    def save_model(self, request, obj, form, change) -> None:
        password = request.POST.get('form-0-password')
        if change and password:
            obj.set_password(password)
            obj.save()

        super().save_model(request, obj, form, change)
