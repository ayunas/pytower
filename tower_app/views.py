from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect

from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.template.defaulttags import csrf_token
from django import forms

from .forms import UserRegistrationForm

import json

# Create your views here.
def test(request):
    return HttpResponse('test is working properly')

def index(request):
    return HttpResponse('this is the index page view function')

def loginView(request):
    return render(request, "auth/login.html")

def register(request):
    return render(request, "auth/register.html")

def loginPost(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/test')
            else:
                form.add_error("username", "Username or password incorrect")
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})

def registerPost(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            password =  userObj['password1']
            if not (User.objects.filter(username=username).exists()):
                user = form.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return HttpResponseRedirect('/test')
            else:
                form.add_error("username", "that username is already taken")
        else:
            form.add_error("password1", "Check to make sure your password fills requirements")
                
    else:
        form = UserCreationForm()
        
    return render(request, 'auth/register.html', {'form' : form})
    