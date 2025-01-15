from django.contrib import admin
from .models import PageView, CustomUser, Hobby
from django.contrib.auth.admin import UserAdmin


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for the PageView model.
    """
    list_display = ['page_name', 'user', 'count']
    search_fields = ['page_name', 'user__username']  # Updated to match the user field in the database
    list_filter = ['page_name', 'user']
    ordering = ['page_name', 'count']  # Added ordering for better organization


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin panel configuration for the CustomUser model.
    Extends the default UserAdmin to include additional fields.
    """
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('name', 'date_of_birth')}),
    )
    list_display = ['username', 'email', 'name', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'name']
    list_filter = ['is_staff', 'is_active', 'date_joined']
    ordering = ['username']  # Ensures users are listed alphabetically


@admin.register(Hobby)
class HobbyAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for the Hobby model.
    """
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']  # Ensure hobbies are listed alphabetically
