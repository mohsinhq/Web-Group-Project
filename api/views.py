from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from .models import PageView, CustomUser


def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})


# Test view to display PageView count
def page_view_count(request):
    page_view, created = PageView.objects.get_or_create(id=1)
    page_view.count += 1
    page_view.save()
    return JsonResponse({"Page View Count": page_view.count})

# View to display user list (for testing purposes)
def user_list(request):
    users = CustomUser.objects.values("username", "date_of_birth", "hobbies")
    return JsonResponse({"users": list(users)})