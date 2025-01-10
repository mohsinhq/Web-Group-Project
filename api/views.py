from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import json
from .models import PageView, CustomUser
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm


def main_spa(request: HttpRequest) -> JsonResponse:
    return render(request, 'api/spa/index.html', {})


# Test view to display PageView count
def page_view_count(request):
    page_view, _ = PageView.objects.get_or_create(id=1)
    page_view.count += 1
    page_view.save()
    return JsonResponse({"Page View Count": page_view.count})


# View to display user list (for testing purposes)
def user_list(request):
    users = CustomUser.objects.values("username", "date_of_birth", "hobbies")
    return JsonResponse({"users": list(users)})


# Signup view
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Parse JSON data from Vue
        form = CustomUserCreationForm(data)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({"message": "Signup successful"}, status=201)
        else:
            return JsonResponse({"error": form.errors}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=json.loads(request.body))
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return JsonResponse({
                'id': user.id,
                'username': user.username,
                'name': user.name,
                'email': user.email,
                'hobbies': user.hobbies,
            })
        else:
            return JsonResponse({"error": form.errors}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


# Logout View
def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Logged out successfully'})


# User profile data
def user_data(request):
    if request.user.is_authenticated:
        user = request.user
        return JsonResponse({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'date_of_birth': user.date_of_birth,
            'hobbies': user.hobbies,
        })
    return JsonResponse({'error': 'User not authenticated'}, status=401)
