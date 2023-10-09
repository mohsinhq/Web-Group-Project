from django.contrib import admin

from .models import PageView

# Register your models here.


class PageViewAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'ip_address']


admin.site.register(PageView, PageViewAdmin)
