from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect

from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.template.defaulttags import csrf_token
from django import forms

from .forms import UserRegistrationForm

import json
from django.http import HttpResponse, HttpResponseRedirect
from .forms import CreateCharacter, MoveCharacter
from .models import Player, Room, Item

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


def play(request, id):
    print("REFRESH")
    character=Player.objects.get(id=id)
    inventory=character.inventory()
    poison = Item.objects.get(item_name="Rat Poison")
    print("poison room id", poison.roomID)
    if len(inventory) == 0:
        inventory=None
    rooms = Room.objects.filter(floor=character.room.floor)
    #room_items=Item.objects.all()
    room_items = character.room.items()
    print(f"player current room ID: {character.room.id}")
    if len(room_items) == 0:
        room_items = None
    else:
        
        #print(f"ROOM_ITEMS")
        for item in room_items:
            print(f"item_name: {item.item_name}, roomID: {item.roomID}")
    message=None
    #print("ROOM", character.room.room_name)

    if request.method =="POST":
        #print("method is post")

        form = MoveCharacter(request.POST)
        if form.is_valid():
            #print("form is valid")
            action=form.cleaned_data.get("btn")
            #print("ACTION", action)
            #TODO: complete these once models are finished
            if action.startswith("t"):
                #print("TAKE")
                item_name=action[5:]
                #print("ITEM", item_name)
                message=character.pickup(item_name)
                return HttpResponseRedirect(f'/play/{character.id}')
            elif action=="drop":
                pass
            elif action=="attack":
                pass
            
            else:
                print("move")
                message=character.move(action)
                return HttpResponseRedirect(f'/play/{character.id}')
        else:
            form = MoveCharacter()

    context = {"player": character, "rooms": rooms, "inventory": inventory, "items": room_items, "message": message}
    print(f"inventory: {inventory} \nroom_items:{room_items}\nmessage: {message}")
#    player ={"name": "Player1", "location": "Foyer"}
    return render(request, "tower_app/play.html", context)
