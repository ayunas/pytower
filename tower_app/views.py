from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import CreateCharacter, MoveCharacter, UserRegistrationForm
from .models import Player, Room, Item
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect

from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.template.defaulttags import csrf_token
from django import forms

import json

# Create your views here.
def test(request):
    return HttpResponse('test is working properly')

def start(request):
    if request.method == "POST":
        form = CreateCharacter(request.POST)
        if form.is_valid():
            n = form.cleaned_data["name"]
            character = Player(name=n)
            character.initialize()
            character.save()
            character=Player.objects.get(id=character.id)

        return HttpResponseRedirect(f'/play/{character.id}')
    else:
        form= CreateCharacter()

    return render(request, "tower_app/index.html", {"form": form})

def get_context(player_id, message=None):
    player=Player.objects.get(id=player_id)
    inventory=player.inventory()
    if len(inventory) == 0:
        inventory=None
    room_items = player.room.items()
    if len(room_items) == 0:
        room_items = None
    #TODO: change this later
    #rooms = Room.objects.filter(floor=character.room.floor)
    rooms = Room.objects.filter(floor=1)
    #if character.room.floor>1:
    #    minus = (character.room.floor-1) * 11
    #    print("MINUS", minus)
    #    for room in rooms:
    #        room.id=room.id-minus
    return {"player": player, "rooms": rooms, "inventory": inventory, "items": room_items, "message": message}

def play(request, id):
    player_id=id
    context=get_context(player_id)
    print("Context", context)
    print("REFRESH")
    if request.method =="POST":
        #print("method is post")
        form = MoveCharacter(request.POST)
        if form.is_valid():
            #print("form is valid")
            action=form.cleaned_data.get("btn")
            #print("ACTION", action)
            #TODO: complete drop function models
            if action.startswith("take"):
                #print("TAKE")
                item_name=action[5:]
                #print("ITEM", item_name)
                message=context["player"].pickup(item_name)
                context=get_context(player_id, message)
                print("Context", context)
                #return HttpResponseRedirect(f'/play/{character.id}')
            elif action.startswith("drop"):
                item_name=action[5:]
                message=context["player"].drop(item_name)

                context=get_context(player_id, message)
                print("Context", context)
            elif action=="attack":
                pass
            
            else:
                print("move")
                message=context["player"].move(action)
                context=get_context(player_id, message)
                print("Context", context)
                #return HttpResponseRedirect(f'/play/{character.id}')
        else:
            form = MoveCharacter()

    #print(f"inventory: {inventory} \nroom_items:{room_items}\nmessage: {message}")
#    player ={"name": "Player1", "location": "Foyer"}
    return render(request, "tower_app/play.html", context)

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
                return HttpResponseRedirect('/start')
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
    
