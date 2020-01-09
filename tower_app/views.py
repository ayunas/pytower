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
            character.save()
            character=Player.objects.get(id=character.id)
            print("Index ID", character.id)
            room=character.initialize("y")
            print("INDEX ROOM", character.room)
#            character = Player.objects.get(id=character.id)
            print("INDEX ROOM after GET", character.room)

        return HttpResponseRedirect(f'/play/{character.id}')
    else:
        form= CreateCharacter()

    return render(request, "tower_app/index.html", {"form": form})
#TODO: once model is done, change player so it's not hard coded, .ay need to change "id"
def play(request, id):
    character=Player.objects.get(id=id)
    room = Room.objects.get(room_name=character.room)
    #print("Play CHARACTER", character)
    #print("Play ID", id)
    #print("PLAY ROOM", character.room)
    context = {"player": character, "room": room}
    if request.method =="POST":
    #    print("request.POST", request.POST)
        form = MoveCharacter(request.POST)
        if form.is_valid():
            data=form.cleaned_data.get("btn")
            #TODO: complete these once models are finished
            if data=="take":
                pass
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