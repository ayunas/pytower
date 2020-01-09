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
    character=Player.objects.get(id=id)
    inventory=character.inventory()
    rooms = Room.objects.filter(floor=character.room.floor)
    room_items=Item.objects.all()
    print("ROOM_ITEMS", room_items)
    #room_items = character.room.items()
    message=None
    print("ROOM", character.room.room_name)

    if character.room.room_name == "Staircase":
        message="Move right to go upstairs"

    if request.method =="POST":

        form = MoveCharacter(request.POST)
        if form.is_valid():
            data=form.cleaned_data.get("btn")
            #TODO: complete these once models are finished
            if data=="take":
                    message=character.pickup(room_items.item_name)

            elif data=="drop":
                pass
            elif data=="attack":
                pass
            
            else:
                message=character.move(data)
        else:
            form = MoveCharacter()

    context = {"player": character, "rooms": rooms, "inventory": inventory, "items": room_items, "message": message}
    print(f"inventory: {inventory} \nroom_items:{room_items}\nmessage: {message}")
#    player ={"name": "Player1", "location": "Foyer"}
    return render(request, "tower_app/play.html", context)