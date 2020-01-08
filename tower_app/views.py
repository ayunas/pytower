from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import CreateCharacter, MoveCharacter
from .models import Player

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
            character=Player.objects.get(uuid=character.uuid)
            character.initialize()

        return HttpResponseRedirect(f'/play/{character.uuid}')
    else:
        form= CreateCharacter()

    return render(request, "tower_app/index.html", {"form": form})
#TODO: once model is done, change player so it's not hard coded, .ay need to change "id"
def play(request, uuid):
    character=Player.objects.get(uuid=uuid)
    print("CHARACTER", character)
    context = {"player": character}
    if request.method =="POST":
        print("request.POST", request.POST)
        form = MoveCharacter(request.POST)
        if form.is_valid():
            data=form.cleaned_data.get("btn")
            #TODO: once other methods are added, this will need to change
            character.move(data)
            print("FORM DATA", data)
    else:
        form = MoveCharacter()


#    player ={"name": "Player1", "location": "Foyer"}
    return render(request, "tower_app/play.html", context)