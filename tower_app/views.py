from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def test(request):
    return HttpResponse('test is working properly')

def index(request):
    return HttpResponse('this is the index page view function')

def login(request):
    return render(request, "auth/login.html")

def register(request):
    return render(request, "auth/register.html")