from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import UserChangeForm
from django.views.decorators.csrf import csrf_exempt
from .models import Hobby
from django.core.exceptions import ValidationError
import json


def main_spa(request: HttpRequest) -> HttpResponse:
    """Render the main Single Page Application."""
    return render(request, 'api/spa/index.html', {})

@login_required
def get_user_data(request: HttpRequest) -> JsonResponse:
    """API endpoint to fetch authenticated user data."""
    user = request.user
    return JsonResponse({
        "name": user.name,
        "email": user.email,
        "date_of_birth": user.date_of_birth,
        "hobbies": user.hobbies,
    })

def signup_view(request: HttpRequest) -> HttpResponse:
    """Render the signup page and handle user registration."""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after signup
            return redirect('/')  # Redirect to the SPA
    else:
        form = CustomUserCreationForm()
    return render(request, 'api/signup.html', {'form': form})

def login_view(request: HttpRequest) -> HttpResponse:
    """Render the login page and handle user authentication."""
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Log the user in
            return redirect('/')  # Redirect to the SPA
    else:
        form = AuthenticationForm()
    return render(request, 'api/login.html', {'form': form})

def logout_view(request: HttpRequest) -> HttpResponse:
    """Logout a user and redirect to the login page."""
    logout(request)
    return redirect('/login/')

@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    """Render and handle the profile page."""
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/')  # Redirect back to SPA
    else:
        form = CustomUserChangeForm(instance=request.user)
        form.fields.pop('password', None)  # Exclude the password field from the form
    return render(request, 'api/profile.html', {'form': form})


@csrf_exempt
def hobbies_view(request):
    if request.method == 'GET':
        hobbies = Hobby.objects.all()
        hobby_data = [{"id": hobby.id, "name": hobby.name} for hobby in hobbies]
        return JsonResponse(hobby_data, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            hobby_name = data.get('name')
            new_hobby = Hobby.objects.create(name=hobby_name)
            return JsonResponse({"id": new_hobby.id, "name": new_hobby.name}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
@login_required
def hobbies_api(request):
    if request.method == "GET":
        hobbies = Hobby.objects.all().values("id", "name")
        return JsonResponse({"hobbies": list(hobbies)}, safe=False)
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            hobby_name = data.get("name")
            hobby, created = Hobby.objects.get_or_create(name=hobby_name)
            if created:
                # Return hobby data when it's created
                return JsonResponse({"message": "Hobby added successfully", "hobby": {"id": hobby.id, "name": hobby.name}}, status=201)
            else:
                return JsonResponse({"error": "Hobby already exists"}, status=400)
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception:
            return JsonResponse({"error": "Invalid data"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)