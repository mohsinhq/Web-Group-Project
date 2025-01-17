"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse

from . import views
from .views import main_spa


urlpatterns = [
    path('', main_spa),
    path('pageviews/', views.page_view_count, name='pageviews'),  # Endpoint for testing PageView count
    path('users/', views.user_list, name='user_list'), # Endpoint for user list (for testing purposes)
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),  # Home route for Vue SPA
    path('user_data/', views.user_data, name='user_data'),  # API for fetching authenticated user data
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
