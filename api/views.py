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
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Hobby, FriendRequest
from django.db import models  # Import models to use Q objects
from .models import CustomUser, Hobby, FriendRequest, Friendship  # Import Friendship model
from django.http import JsonResponse
from .models import FriendRequest



@login_required
def send_friend_request(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        data = json.loads(request.body)
        to_user_id = data.get("user_id")

        if not to_user_id:
            return JsonResponse({"error": "User ID is required."}, status=400)

        to_user = CustomUser.objects.filter(id=to_user_id).first()
        if not to_user:
            return JsonResponse({"error": "User not found."}, status=404)

        if FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
            return JsonResponse({"error": "You have already sent a friend request to this user."}, status=400)

        if FriendRequest.objects.filter(from_user=to_user, to_user=request.user).exists():
            return JsonResponse({"error": "This user has already sent you a friend request."}, status=400)

        # Additional check for existing friendship
        if to_user in request.user.friends.all():
            return JsonResponse({"error": "You are already friends with this user."}, status=400)

        # Create a new FriendRequest
        FriendRequest.objects.create(from_user=request.user, to_user=to_user)
        return JsonResponse({"message": "Friend request sent!"}, status=200)

    return JsonResponse({"error": "Invalid request method."}, status=405)


@login_required
def friend_requests_api(request: HttpRequest) -> JsonResponse:
    """
    API endpoint to retrieve pending friend requests for the logged-in user.
    """
    if request.method == "GET":
        pending_requests = FriendRequest.objects.filter(to_user=request.user, status="pending").select_related("from_user")
        data = [
            {
                "id": req.id,
                "from_user": {
                    "id": req.from_user.id,
                    "name": req.from_user.name,
                },
                "status": req.status,
            }
            for req in pending_requests
        ]
        return JsonResponse({"requests": data}, safe=False)
    return JsonResponse({"error": "Invalid request method."}, status=405)



@login_required
def friends_list_api(request: HttpRequest) -> JsonResponse:
    if request.method == "GET":
        friendships = Friendship.objects.filter(
            models.Q(user1=request.user) | models.Q(user2=request.user)
        )
        data = [
            {
                "id": friend.user2.id if friend.user1 == request.user else friend.user1.id,
                "name": friend.user2.name if friend.user1 == request.user else friend.user1.name,
            }
            for friend in friendships
        ]
        return JsonResponse({"friends": data}, safe=False)
    return JsonResponse({"error": "Invalid request method."}, status=405)


@login_required
def remove_friend(request: HttpRequest) -> JsonResponse:
    """
    API endpoint to remove a friend.
    """
    if request.method == "POST":
        data = json.loads(request.body)
        friend_id = data.get("friend_id")

        if not friend_id:
            return JsonResponse({"error": "Friend ID is required."}, status=400)

        # Find the friend user
        friend = CustomUser.objects.filter(id=friend_id).first()
        if not friend:
            return JsonResponse({"error": "Friend not found."}, status=404)

        # Check if the friendship exists
        friendship = Friendship.objects.filter(
            models.Q(user1=request.user, user2=friend) | models.Q(user1=friend, user2=request.user)
        ).first()

        if not friendship:
            return JsonResponse({"error": "This user is not your friend."}, status=400)

        # Remove the friendship
        friendship.delete()

        return JsonResponse({"message": "Friend removed successfully."}, status=200)

    return JsonResponse({"error": "Invalid request method."}, status=405)




@login_required
def respond_friend_request(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        data = json.loads(request.body)
        request_id = data.get("request_id")
        action = data.get("action")

        if not request_id or not action:
            return JsonResponse({"error": "Request ID and action are required."}, status=400)

        friend_request = FriendRequest.objects.filter(id=request_id, to_user=request.user).first()
        if not friend_request:
            return JsonResponse({"error": "Friend request not found."}, status=404)

        if action not in ["accept", "reject"]:
            return JsonResponse({"error": "Invalid action."}, status=400)

        if action == "accept":
            friend_request.status = "accepted"
            # Create a mutual friendship
            Friendship.objects.create(user1=request.user, user2=friend_request.from_user)
        elif action == "reject":
            friend_request.status = "rejected"

        friend_request.save()
        return JsonResponse({"message": f"Friend request {action}ed!"}, status=200)

    return JsonResponse({"error": "Invalid request method."}, status=405)



@login_required
def similar_users_api(request: HttpRequest) -> JsonResponse:
    """
    API to retrieve a list of users sorted by hobby similarity to the logged-in user.
    Supports filtering by age and pagination.
    """
    user = request.user
    user_hobbies = user.user_hobbies.all()

    # Get all other users except the logged-in user
    users = CustomUser.objects.exclude(id=user.id)

    # Count hobbies in common
    users_with_common_hobbies = []
    for other_user in users:
        common_hobbies = user_hobbies.intersection(other_user.user_hobbies.all())
        users_with_common_hobbies.append({
            "id": other_user.id,
            "name": other_user.name,
            "age": other_user.get_age(),  # Custom method to calculate age
            "hobby_count": len(common_hobbies),
            "hobbies": list(common_hobbies.values("id", "name")),
        })

    # Sort users by hobby_count in descending order
    users_with_common_hobbies.sort(key=lambda x: x["hobby_count"], reverse=True)

    # Filter by age if provided
    min_age = request.GET.get("min_age")
    max_age = request.GET.get("max_age")
    if min_age or max_age:
        min_age = int(min_age) if min_age else None
        max_age = int(max_age) if max_age else None
        users_with_common_hobbies = [
            user for user in users_with_common_hobbies
            if (min_age is None or user["age"] >= min_age) and (max_age is None or user["age"] <= max_age)
        ]

    # Paginate results
    paginator = Paginator(users_with_common_hobbies, 10)  # Show 10 users per page
    page_number = request.GET.get("page", 1)
    page = paginator.get_page(page_number)

    return JsonResponse({
        "users": list(page.object_list),
        "has_next": page.has_next(),
        "has_previous": page.has_previous(),
        "current_page": page.number,
    })


@login_required
def change_password_view(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            old_password = data.get("old_password")
            new_password = data.get("new_password")
            confirm_password = data.get("confirm_password")

            if not old_password or not new_password or not confirm_password:
                return JsonResponse({"error": "All fields are required"}, status=400)

            if new_password != confirm_password:
                return JsonResponse({"error": "New passwords do not match"}, status=400)

            user = request.user
            if not user.check_password(old_password):
                return JsonResponse({"error": "Old password is incorrect"}, status=400)

            try:
                validate_password(new_password, user=user)
            except ValidationError as e:
                return JsonResponse({"error": list(e.messages)}, status=400)

            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Prevent session logout after password change
            return JsonResponse({"message": "Password updated successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)


def main_spa(request):
    if not request.user.is_authenticated:
        return redirect('api:login')  # Redirect to login if user is not authenticated
    return render(request, 'api/spa/index.html')


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('api:main-spa')  # Redirect to main SPA
    else:
        form = AuthenticationForm()
    return render(request, 'api/login.html', {'form': form})


def hobbies_api(request: HttpRequest) -> JsonResponse:
    """
    API endpoint to retrieve all hobbies.
    """
    if request.method == "GET":
        hobbies = Hobby.objects.all().values("id", "name")
        return JsonResponse({"hobbies": list(hobbies)}, safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=405)







def logout_view(request):
    logout(request)
    return redirect(reverse('api:login'))  # Redirect to login after logout




def get_user_data(request: HttpRequest) -> JsonResponse:
    """
    API endpoint to retrieve authenticated user data.
    """
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Unauthorized"}, status=401)
    user = request.user
    return JsonResponse({
        "name": user.name,
        "email": user.email,
        "date_of_birth": user.date_of_birth,
        "hobbies": list(user.user_hobbies.values("id", "name")),  # Fixed hobbies to reflect ManyToMany relation
    })


def signup_view(request):
    """
    Handles user signup and registration.
    """
    if request.method == "POST":
        print("Signup POST data:", request.POST)  # Debugging POST data
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('api:login')  # Redirect to login after successful signup
        else:
            print("Form errors:", form.errors)  # Debugging form errors
            return render(request, 'api/signup.html', {'form': form})  # Display errors
    else:
        form = CustomUserCreationForm()
    return render(request, 'api/signup.html', {'form': form})


@login_required
def profile_view(request: HttpRequest) -> JsonResponse:
    """
    Handles GET and POST requests for user profile data.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = request.user
            user.name = data.get("name", user.name)
            user.email = data.get("email", user.email)
            user.date_of_birth = data.get("date_of_birth", user.date_of_birth)

            # Update ManyToMany relationship for hobbies
            hobbies = data.get("hobbies", [])
            user.user_hobbies.set(Hobby.objects.filter(id__in=hobbies))

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
            "hobbies": list(user.user_hobbies.values("id", "name")),  # Send hobbies as a list
        })
    return JsonResponse({"error": "Invalid request method"}, status=405)
