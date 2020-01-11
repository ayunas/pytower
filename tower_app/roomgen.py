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

def stairs(pk,floor):
    stairs = {}
    stairs['model'] = "tower_app.room"
    stairs["pk"] = pk
    stairs["fields"] = {
        'id' : pk,
        'room_name': 'Staircase',
        'description': "Movin' On Up!!!",
        'up': '',
        'down': '',
        'left': '',
        'right': '',
        'floor':floor
    }
    stairs["fields"]['up'] = names[3]
    stairs['fields']['left'] = names[5]
    stairs['fields']['right'] = names[11]
    return stairs

def treasure():
    treasure = {}
    treasure['model'] = "tower_app.room"
    treasure["pk"] = 110
    treasure["fields"] = {
        'id' : 110,
        'room_name': 'Treasure',
        'description': "Made it to the top! Remember though, Money isn't everything",
        'up': '',
        'down': '',
        'left': '',
        'right': '',
        'floor': 10
    }
    
    return treasure

def roomgen(names,descriptions):
    pk = 12
    rooms = []
    floor = 2

    while floor <= 10:
        for i in range(10):
            room = {}
            room['model'] = "tower_app.room"
            room["pk"] = pk
            room["fields"] = {
                'id' : pk,
                'room_name': names[i],
                'description': descriptions[i],
                'up': '',
                'down': '',
                'left': '',
                'right': '',
                'floor':floor
            }
            if i == 0:
                room["fields"]['up'] = names[7]
                room['fields']['right'] = names[1]
            if i == 1:
                room["fields"]['up'] = names[6]
                room['fields']['left'] = names[0]
                room['fields']['right'] = names[2]
            if i == 2:
                room["fields"]['down'] = names[5]
                room['fields']['left'] = names[1]
                room['fields']['right'] = names[3]
            if i == 3:
                room["fields"]['down'] = "Staircase"
                room['fields']['left'] = names[2]
            if i == 4:
                room['fields']['right'] = names[8]
            if i == 5:
                room["fields"]['up'] = names[2]
                room['fields']['right'] = "Staircase"
            if i == 6:
                room["fields"]['down'] = names[1]
                room['fields']['left'] = names[7]
            if i == 7:
                room["fields"]['up'] = names[8]
                room['fields']['down'] = names[0]
                room['fields']['right'] = names[6]
            if i == 8:
                room["fields"]['up'] = names[9]
                room['fields']['down'] = names[7]
                room['fields']['left'] = names[4]
            if i == 9:
                room['fields']['down'] = names[8]
            # if i == 10:
                # room["fields"]['up'] = names[3]
                # room['fields']['left'] = names[5]
                # room['fields']['right'] = names[11]
            rooms.append(room)
            pk = pk + 1
        if floor == 10:
            rooms.append(treasure())
        else:
            rooms.append(stairs(pk,floor))
            pk = pk + 1
        floor = floor + 1
        # del names[:9]
        # del descriptions[:9]
        names = names[10:]
        descriptions = descriptions[10:]
    return rooms

roomgen(names,descriptions)

with open('./fixtures/roomgen_fixture.json', 'w') as file:
    json.dump(roomgen(names,descriptions),file,indent=2)
