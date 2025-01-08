from django.http import JsonResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
import json
from .models import PageView, CustomUser


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
