from django.contrib import admin
from .models import PageView, CustomUser, Hobby
from django.contrib.auth.admin import UserAdmin

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ['page_name', 'user', 'count']
    search_fields = ['page_name', 'user__name']
    list_filter = ['page_name', 'user']


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('name', 'date_of_birth', 'hobbies')}),
    )
    list_display = ['username', 'email', 'name', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'name']
    list_filter = ['is_staff', 'is_active', 'date_joined']


@admin.register(Hobby)
class HobbyAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
