from django.contrib import admin
from .models import CustomUser, PageView

# Register CustomUser
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_of_birth', 'hobbies')
    search_fields = ('username', 'email')

# Register PageView
@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ('count',)
