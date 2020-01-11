from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import CreateCharacter, MoveCharacter, UserRegistrationForm
from .models import Player, Room, Item, Enemy
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
    for item in inventory:
        print(item.item_name)
    if len(inventory) == 0:
        inventory=None
    room_items = player.room.items()
    if len(room_items) == 0:
        room_items = None
    enemies = Enemy.objects.filter(roomID=player.room.id)
    if len(enemies) == 0:
        enemies = None
    rooms = Room.objects.filter(floor=player.room.floor)

    return {"player": player, "rooms": rooms, "inventory": inventory, "items": room_items, "message": message, "enemies": enemies}

def play(request, id):
    player_id=id
    context=get_context(player_id)
    #print("Context", context["player"].room.room_name)
    print("REFRESH")
    if request.method =="POST":
        #print("method is post")
        form = MoveCharacter(request.POST)
        if form.is_valid():
            #print("form is valid")
            action=form.cleaned_data.get("btn")
            print("ACTION", action)
            #TODO: complete drop function models
            if action.startswith("take"):
                #print("TAKE")
                item_name=action[5:]
                #print("ITEM", item_name)
                message=context["player"].pickup(item_name)
                context=get_context(player_id, message)

            elif action.startswith("drop"):
                item_name=action[5:]
                message=context["player"].drop(item_name)

                context=get_context(player_id, message)

            elif action.startswith("attack"):
                action_enemy_name=action[7:]
                print(f"ATTACKING ENEMY {action_enemy_name}")
                if context["enemies"] is not None:
                    for enemy in context["enemies"]:
                        print(f"ENEMY: {enemy.enemy_name}")
                        print(f".{enemy.enemy_name}., .{action_enemy_name}.")
                        if enemy.enemy_name == action_enemy_name:
                            print("ENEMY.Enemy_name = action_enemy_name")
                            message = enemy.player_strikes_enemy(context["player"])
                            context=get_context(player_id, message)
                            break
                        else:
                            print("ENEMY DOES NOT MATCH")
            
            else:
                print("ELSE")
                message=context["player"].move(action)
                context=get_context(player_id, message)

        else:
            form = MoveCharacter()

    context["rm10ids"] = [10,21,32,43,54,65,76,87,98,109]
    context["rm9ids"] = [9, 20,31,42,53,64,75,86,97,108]
    context["rm8ids"] = [8,19,30,41,52,63,74,85,96,107]
    context["rm7ids"] = [7,18,29,40,51,62,73,84,95,106]
    context["rm6ids"] = [6,17,28,39,50,61,72,83,94,105]
    context["rm5ids"] = [5,16,27,38,49,60,71,82,93,104]
    context["rm4ids"] = [4,15,26,37,48,59,70,81,92,103]
    context["rm3ids"] = [3,14,25,36,47,58,69,80,91,102]
    context["rm2ids"] = [2,13,24,35,46,57,68,79,90,101]
    context["rm1ids"] = [1,12,23,34,45,56,67,78,89,100]
    context["stairids"] = [11,22,33,44,55,66,77,88,99]
    context["outsideids"]= [0]

    return render(request, "tower_app/play.html", context)


def loginView(request):
    return render(request, "auth/login.html")


def register(request):
    return render(request, "auth/register.html")


def loginPost(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
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
            password = userObj['password1']
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
    
