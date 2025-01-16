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
from .views import main_spa, login_view, logout_view, signup_view, profile_view, hobbies_api, get_user_data, change_password_view
from .views import similar_users_api, respond_friend_request
from .views import send_friend_request, friend_requests_api, friends_list_api, remove_friend


app_name = 'api'

urlpatterns = [
    path('', main_spa, name='main-spa'),  # Main SPA
    path('login/', login_view, name='login'),  # Login
    path('logout/', logout_view, name='logout'),  # Logout
    path('signup/', signup_view, name='signup'),  # Signup
    path('profile/', profile_view, name='profile'),  # Profile API
    path('hobbies/', hobbies_api, name='hobbies-api'),  # Hobbies API
    path('user-data/', get_user_data, name='user-data'),  # User Data API
    path('change-password/', change_password_view, name='change-password'),
    path('similar-users/', similar_users_api, name='similar-users'),  # Change Password API
    path("respond-friend-request/", respond_friend_request, name="respond-friend-request"),
    path("send-friend-request/", send_friend_request, name="send-friend-request"),
    path("friend-requests/", friend_requests_api, name="friend-requests"),
    path("friends-list/", friends_list_api, name="friends-list"),
    path("remove-friend/", remove_friend, name="remove-friend"),
]








