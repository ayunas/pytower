from random import randint, choice
import json

enemies = ['Giant Scorpion Spider',
           'Reaper',
           'Ogre',
           'Troll',
           'Creeper',
           'Witch',
           'Red Dragon',
           'Stone Beast',
           'Warlock',
           'Goblin']


def enemy_gen(enemies):
    i = 101
    e = []
    while i < 110:
        enemy = {}
        enemy_name = choice(enemies)
        enemy['model'] = "tower_app.item"
        enemy["pk"] = i
        enemy["fields"] = {
            # 'id' : 1,
            'enemy_name': enemy_name,
            'strength': randint(1, 11),
            'HP': randint(1, 11),
            'description': f"{enemy_name} fights",
            'roomID': randint(1, 110)
        }
        e.append(enemy)
        i = i + 1
    return e


with open('../tower_app/fixtures/enemies_fixture.json', 'w') as file:
    json.dump(enemy_gen(enemies), file, indent=2)
