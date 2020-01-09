import json,random,requests

words = requests.get("http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain").content.splitlines()

names = []
descriptions = []

for i in range(100):
    random_word = str(random.choice(words)).replace("b\'",'').capitalize()
    names.append(random_word)
    descriptions.append(f'Description for the {random_word} room ')

# names = ['Emerald','Diamond','Ruby','Purgatory','Gully','Lair','Dungeon','Cabbage Patch','Tea','Staircase']
# descriptions = ['description1', 'description2', 'desription3']

def roomgen():
    pk = 12
    rooms = []
    for i in range(10):
        room = {}
        room['model'] = "tower_app.room"
        room["pk"] = pk + 1
        room["fields"] = {
            'id' : pk + 1,
            'room_name': names[i],
            'description': descriptions[i],
            'up': '',
            'down': '',
            'left': '',
            'right': '',
            'floor':2
        }
        rooms.append(room)
        pk = pk + 1

    return rooms

roomgen()

with open('./fixtures/roomgen_fixture.json', 'w') as file:
    json.dump(roomgen(),file,indent=2)


# pk = 13

# room = {}
# room.model = "tower_app.room"
# room.pk = pk + 1
# room.fields = {
#     'id' : pk + 1
# }

# pk = pk + 1


    # "model": "tower_app.room",
    # "pk": 0,
    # "fields": {
    #   "id":0,
    #   "room_name": "Outside",
    #   "description": " you are outside the PyTower. It is a 10 story tower. There is a treasure chest on the top floor. Do you have what it takes to reach the top???",
    #   "up" : "",
    #   "down" : "",
    #   "left": "",
    #   "right": "Foyer",
    #   "floor": 1
    # }