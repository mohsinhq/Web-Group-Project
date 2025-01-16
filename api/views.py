from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.conf import settings
from .forms import CustomUserCreationForm
from .models import Hobby, CustomUser
import json
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required



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

def logout_view(request):
    logout(request)
    return redirect(reverse('api:login'))  # Redirect to login after logout


@login_required
def hobbies_api(request: HttpRequest) -> JsonResponse:
    """
    API endpoint to retrieve all hobbies.
    """
    if request.method == "GET":
        hobbies = Hobby.objects.all().values("id", "name")
        return JsonResponse({"hobbies": list(hobbies)}, safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=405)


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


def signup_view(request: HttpRequest) -> HttpResponse:
    """
    Handles user signup and registration.
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user but do NOT log them in
            return redirect(reverse('api:login'))  # Redirect to login
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

def user_list(request):
    min_age = request.GET.get('min_age')
    max_age = request.GET.get('max_age')

    users = CustomUser.objects.all()

    if min_age:
        users = users.filter(date_of_birth__lte=datetime.now() - timedelta(days=int(min_age) * 365))
    if max_age:
        users = users.filter(date_of_birth__gte=datetime.now() - timedelta(days=int(max_age) * 365))

    users_with_similarity = []

    for user in users:
        similarity_list = []

        for other_user in users:
            if user != other_user:
                common_hobbies_count = user.common_hobbies(other_user)
                similarity_list.append({
                    'user': other_user.as_dict(),
                    'common_hobbies': common_hobbies_count,
                })

        sorted_similarity = sorted(similarity_list, key=lambda x: x['common_hobbies'], reverse=True)

        users_with_similarity.append({
            'user': user.as_dict(),
            'similar_users': sorted_similarity[:10],
        })

    page_number = request.GET.get('page', 1)
    per_page = int(request.GET.get('per_page', 10))
    paginator = Paginator(users_with_similarity, per_page)
    page = paginator.get_page(page_number)

    return JsonResponse({
        'users': page.object_list,
        'total_pages': paginator.num_pages,
        'current_page': page.number,
    })

