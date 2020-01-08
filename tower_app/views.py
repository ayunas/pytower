from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import CreateCharacter
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
            id=Player.objects.get(id=character.id)
        return HttpResponseRedirect(f'/play/{id}')
    else:
        form= CreateCharacter()

    return render(request, "tower_app/index.html", {"form": form})
#TODO: once model is done, change player so it's not hard coded, .ay need to change "id"
def play(request, uuid):
    #player = Player.objects.get(uuid=uuid)
    player ={"name": "Player1", "location": "Foyer"}
    return render(request, "tower_app/play.html", player)