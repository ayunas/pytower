from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import CreateCharacter, MoveCharacter
from .models import Player, Room

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
    room_items = character.room.items()
    context = {"player": character, "rooms": rooms, "inventory": inventory, "items": room_items}

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
            if message is not None:
                context["message"]=message
    #        print("FORM DATA", data)
    #        print("MESSAGE", message)
    else:
        form = MoveCharacter()


#    player ={"name": "Player1", "location": "Foyer"}
    return render(request, "tower_app/play.html", context)