from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
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

# SignUp View
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('home')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'api/spa/signup.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
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
        form = AuthenticationForm()
    return render(request, 'api/spa/login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Logged out successfully'})

def login_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)  
        return JsonResponse({'message': 'Login successful'})
    return JsonResponse({'error': 'Invalid credentials'}, status=400)

# Home page for authenticated users
def home(request):
    return render(request, 'api/spa/home.html')

# user_data view to send authenticated user data
def user_data(request):
    if request.user.is_authenticated:
        user = request.user
        return JsonResponse({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'date_of_birth': user.date_of_birth,
            'hobbies': user.hobbies
        })
    return JsonResponse({'error': 'User not authenticated'}, status=401)
def register_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = CustomUser.objects.create_user(
                username=data["username"],
                name=data["name"],
                email=data["email"],
                date_of_birth=data["date_of_birth"],
                password=data["password"],
            )
            user.set_hobbies_from_list(data.get("hobbies", []))
            user.save()
            return JsonResponse({"message": "User registered successfully."}, status=201)
        except KeyError as e:
            return JsonResponse({"error": f"Missing field: {e.args[0]}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method."}, status=405)

def edit_profile(request):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            user = request.user
            user.name = data.get("name", user.name)
            user.email = data.get("email", user.email)
            user.date_of_birth = data.get("date_of_birth", user.date_of_birth)
            user.set_hobbies_from_list(data.get("hobbies", user.get_hobbies_list()))
            user.save()
            return JsonResponse({"message": "Profile updated successfully."})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method."}, status=405)

def user_profile(request):
    user = request.user
    return JsonResponse({
        "username": user.username,
        "name": user.name,
        "email": user.email,
        "date_of_birth": user.date_of_birth,
        "hobbies": user.get_hobbies_list(),
    })
