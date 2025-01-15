from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.conf import settings
from .forms import CustomUserCreationForm
from .models import Hobby
import json
from django.urls import reverse

def main_spa(request: HttpRequest) -> HttpResponse:
    """Redirect to login page and force logout for new session."""
    if request.user.is_authenticated:
        logout(request)  # Log out the user if logged in
    return redirect(reverse('api:login'))  # Include namespace if defined

@login_required
def get_user_data(request: HttpRequest) -> JsonResponse:
    """API endpoint to fetch authenticated user data."""
    user = request.user
    return JsonResponse({
        "name": getattr(user, "name", ""),
        "email": getattr(user, "email", ""),
        "date_of_birth": getattr(user, "date_of_birth", ""),
        "hobbies": getattr(user, "hobbies", ""),
    })

def signup_view(request: HttpRequest) -> HttpResponse:
    """Render the signup page and handle user registration."""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user but do NOT log them in
            return redirect(reverse('login'))  # Redirect to login
    else:
        form = CustomUserCreationForm()
    return render(request, 'api/signup.html', {'form': form})

def login_view(request: HttpRequest) -> HttpResponse:
    """Render the login page and handle user authentication."""
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect(settings.FRONTEND_URL)  # Redirect to frontend
    else:
        form = AuthenticationForm()
    return render(request, 'api/login.html', {'form': form})

def logout_view(request: HttpRequest) -> HttpResponse:
    """Logout a user and redirect to the login page."""
    logout(request)
    return redirect(reverse('login'))

@login_required
def profile_view(request: HttpRequest) -> JsonResponse:
    """Handle GET and POST requests for user profile."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = request.user
            user.name = data.get("name", user.name)
            user.email = data.get("email", user.email)
            user.date_of_birth = data.get("date_of_birth", user.date_of_birth)
            user.hobbies = data.get("hobbies", user.hobbies)
            user.save()
            return JsonResponse({"message": "Profile updated successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    elif request.method == "GET":
        user = request.user
        return JsonResponse({
            "name": user.name,
            "email": user.email,
            "date_of_birth": user.date_of_birth,
            "hobbies": user.hobbies
        })
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
@login_required
def hobbies_api(request):
    """API endpoint for managing hobbies."""
    if request.method == "GET":
        hobbies = Hobby.objects.all().values("id", "name")
        return JsonResponse({"hobbies": list(hobbies)}, safe=False)
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            hobby_name = data.get("name")
            hobby, created = Hobby.objects.get_or_create(name=hobby_name)
            return JsonResponse({
                "message": "Hobby added successfully",
                "hobby": {"id": hobby.id, "name": hobby.name}
            }, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)
