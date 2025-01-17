from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage
from django.urls import reverse
from .forms import CustomUserCreationForm
from .models import CustomUser, Hobby, FriendRequest, Friendship
import json
from django.db import models

@login_required
def send_friend_request(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            to_user_id = data.get("user_id")
            
            if not to_user_id:
                return JsonResponse({"status": "error", "message": "User ID is required."}, status=400)

            to_user = CustomUser.objects.filter(id=to_user_id).first()
            if not to_user:
                return JsonResponse({"status": "error", "message": "User not found."}, status=404)

            # Check if a friend request already exists
            existing_request = FriendRequest.objects.filter(
                from_user=request.user, to_user=to_user
            ).first()

            if existing_request:
                if existing_request.status == "rejected":
                    # Resend rejected request
                    existing_request.status = "pending"
                    existing_request.save()
                    return JsonResponse({"status": "success", "message": "Friend request resent!"}, status=200)
                elif existing_request.status == "pending":
                    return JsonResponse({"status": "error", "message": "Friend request already sent."}, status=400)
                elif existing_request.status == "accepted":
                    return JsonResponse({"status": "error", "message": "You are already friends with this user."}, status=400)

            # Check if the target user has already sent a friend request
            if FriendRequest.objects.filter(from_user=to_user, to_user=request.user, status="pending").exists():
                return JsonResponse({"status": "error", "message": "This user has already sent you a friend request."}, status=400)

            # Check if users are already friends
            if Friendship.objects.filter(
                models.Q(user1=request.user, user2=to_user) | models.Q(user1=to_user, user2=request.user)
            ).exists():
                return JsonResponse({"status": "error", "message": "You are already friends with this user."}, status=400)

            # Create a new friend request
            FriendRequest.objects.create(from_user=request.user, to_user=to_user)
            return JsonResponse({"status": "success", "message": "Friend request sent!"}, status=200)

        except Exception as e:
            return JsonResponse({"status": "error", "message": f"An error occurred: {str(e)}"}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)


@login_required
def friend_requests_api(request: HttpRequest) -> JsonResponse:
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
    if request.method == "POST":
        data = json.loads(request.body)
        friend_id = data.get("friend_id")
        if not friend_id:
            return JsonResponse({"status": "error", "message": "Friend ID is required."}, status=400)

        friend = CustomUser.objects.filter(id=friend_id).first()
        if not friend:
            return JsonResponse({"status": "error", "message": "Friend not found."}, status=404)

        friendship = Friendship.objects.filter(
            models.Q(user1=request.user, user2=friend) | models.Q(user1=friend, user2=request.user)
        ).first()

        if not friendship:
            return JsonResponse({"status": "error", "message": "This user is not your friend."}, status=400)

        friendship.delete()
        FriendRequest.objects.filter(
            models.Q(from_user=request.user, to_user=friend) | models.Q(from_user=friend, to_user=request.user)
        ).delete()

        return JsonResponse({"status": "success", "message": "Friend removed successfully."}, status=200)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)


@login_required
def similar_users_api(request: HttpRequest) -> JsonResponse:
    user = request.user
    user_hobbies = user.user_hobbies.all()
    users = CustomUser.objects.exclude(id=user.id)

    users_with_common_hobbies = []
    for other_user in users:
        common_hobbies = user_hobbies.intersection(other_user.user_hobbies.all())
        users_with_common_hobbies.append({
            "id": other_user.id,
            "name": other_user.name,
            "age": other_user.get_age(),
            "hobby_count": len(common_hobbies),
            "hobbies": list(common_hobbies.values("id", "name")),
        })

    users_with_common_hobbies.sort(key=lambda x: x["hobby_count"], reverse=True)

    min_age = request.GET.get("min_age")
    max_age = request.GET.get("max_age")
    if min_age or max_age:
        min_age = int(min_age) if min_age else None
        max_age = int(max_age) if max_age else None
        users_with_common_hobbies = [
            user for user in users_with_common_hobbies
            if (min_age is None or user["age"] >= min_age) and (max_age is None or user["age"] <= max_age)
        ]

    paginator = Paginator(users_with_common_hobbies, 10)
    page_number = request.GET.get("page", 1)
    try:
        page = paginator.get_page(page_number)
    except EmptyPage:
        return JsonResponse({"error": "Invalid page number."}, status=400)

    return JsonResponse({
        "users": list(page.object_list),
        "has_next": page.has_next(),
        "has_previous": page.has_previous(),
        "current_page": page.number,
    })



@login_required
def respond_friend_request(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        data = json.loads(request.body)
        request_id = data.get("request_id")
        action = data.get("action")

        if not request_id or not action:
            return JsonResponse(
                {"status": "error", "message": "Request ID and action are required."},
                status=400,
            )

        friend_request = FriendRequest.objects.filter(id=request_id, to_user=request.user).first()
        if not friend_request:
            return JsonResponse(
                {"status": "error", "message": "Friend request not found."},
                status=404,
            )

        if action == "accept":
            friend_request.status = "accepted"
            # Check if reverse friend request exists
            reverse_request = FriendRequest.objects.filter(
                from_user=friend_request.to_user, to_user=friend_request.from_user
            ).first()
            if reverse_request:
                reverse_request.delete()

            # Create friendship
            if not Friendship.objects.filter(
                models.Q(user1=request.user, user2=friend_request.from_user)
                | models.Q(user1=friend_request.from_user, user2=request.user)
            ).exists():
                Friendship.objects.create(user1=request.user, user2=friend_request.from_user)

        elif action == "reject":
            friend_request.status = "rejected"
            # Also reject any reverse friend request
            reverse_request = FriendRequest.objects.filter(
                from_user=friend_request.to_user, to_user=friend_request.from_user
            ).first()
            if reverse_request:
                reverse_request.status = "rejected"
                reverse_request.save()

        friend_request.save()
        return JsonResponse(
            {"status": "success", "message": f"Friend request {action}ed!"},
            status=200,
        )

    return JsonResponse(
        {"status": "error", "message": "Invalid request method. Only POST is allowed."},
        status=405,
    )



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
