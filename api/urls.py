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
from django.urls import path
from .views import main_spa, get_user_data, login_view, logout_view, signup_view, profile_view, hobbies_api
from django.contrib.auth import views as auth_views

app_name = 'api'  # Namespacing for reverse lookups

urlpatterns = [
    path('', main_spa, name='main-spa'),  # Main SPA route
    path('user-data/', get_user_data, name='user-data'),  # Fetch user data
    path('signup/', signup_view, name='signup'),  # Signup page
    path('login/', login_view, name='login'),  # Login page
    path('logout/', logout_view, name='logout'),  # Logout page
    path('profile/', profile_view, name='profile'),  # User profile API
    path('hobbies/', hobbies_api, name='hobbies-api'),  # Hobbies API
]


