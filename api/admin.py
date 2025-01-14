from django.contrib import admin
from .models import PageView, CustomUser
from django.contrib.auth.admin import UserAdmin

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ['count']

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('name', 'date_of_birth', 'hobbies')}),
    )
