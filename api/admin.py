from django.contrib import admin
from .models import CustomUser, PageView

# Register CustomUser
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date_of_birth', 'hobbies',)
    list_filter = ('hobbies',)
    search_fields = ('name', 'email',)

# Register PageView
@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ('count',)
