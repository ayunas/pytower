from random import randint, choice
import json

enemy_list = ['Giant Scorpion Spider',
              'Reaper',
              'Ogre',
              'Troll',
              'Creeper',
              'Witch',
              'Red Dragon',
              'Stone Beast',
              'Warlock',
              'Goblin']


def enemy_gen(enemy_list):
    i = 101
    e = []
    while i < 110:
        enemy = {}
        enemy_name = choice(enemy_list)
        enemy['model'] = "tower_app.item"
        enemy["pk"] = i
        enemy["fields"] = {
            # 'id' : 1,
            'item_name': enemy_name,
            'strength': randint(1, 10),
            'item_type': 'armor',
            'description': f"{enemy_name} protects",
            'playerID': None,
            'roomID': randint(1, 110)
        }
        e.append(enemy)
        i = i + 1
    return e


with open('../../../../../Desktop/CS24-BW-MUD/CS24-BW-MUD/tower_app/fixtures/enemies_fixture.json', 'w') as file:
    json.dump(enemy_gen(enemy_list), file, indent=2)
