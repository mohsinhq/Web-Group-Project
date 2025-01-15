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
from .views import main_spa, login_view, logout_view, signup_view, profile_view, hobbies_api, get_user_data

app_name = 'api'

urlpatterns = [
    path('', main_spa, name='main-spa'),  # Main SPA
    path('login/', login_view, name='login'),  # Login
    path('logout/', logout_view, name='logout'),  # Logout
    path('signup/', signup_view, name='signup'),  # Signup
    path('profile/', profile_view, name='profile'),  # Profile API
    path('hobbies/', hobbies_api, name='hobbies-api'),  # Hobbies API
    path('user-data/', get_user_data, name='user-data'),  # User Data API
]







