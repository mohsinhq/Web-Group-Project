from django.shortcuts import render
from django.http import HttpResponse

from .models import PageView

# Create your views here.


def index(request):
    """Takes an request object as a parameter and creates an pageview object then responds by rendering the index view."""
    PageView.objects.create(
        ip_address=request.META.get('REMOTE_ADDR', ''),
    )

    return render(request, 'welcome/index.html', {
        'count': PageView.objects.count()
    })


def health(request):
    """Takes an request as a parameter and gives the count of pageview objects as reponse"""
    return HttpResponse(PageView.objects.count())
