from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import CreateCharacter, MoveCharacter
from .models import Player, Room, Item

# Create your views here.
def test(request):
    return HttpResponse('test is working properly')

def index(request):
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
    #print("REFRESH")
    character=Player.objects.get(id=id)
    print(f"character.floor: {character.floor}")

    inventory=character.inventory()
    if len(inventory) == 0:
        inventory=None

    room_items = character.room.items()
    #print(f"player current room ID: {character.room.id}")
    if len(room_items) == 0:
        room_items = None

    rooms = Room.objects.filter(floor=character.room.floor)
    if character.room.floor>1:
        minus = (character.room.floor-1) * 11
        print("MINUS", minus)
        for room in rooms:
            room.id=room.id-minus

    message=None
    #print("ROOM", character.room.room_name)

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
                message=character.pickup(item_name)
                return HttpResponseRedirect(f'/play/{character.id}')
            elif action.startseith("drop"):
                item_name=action[5:]
                message=character.drop(item_name)
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