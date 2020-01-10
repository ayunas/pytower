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


def enemy_gen(enemies, floor_num):
    # i = 101
    e = []
    start = floor_num + 10 * (floor_num - 1)

    for i in range(floor_num * 2):
        enemy = {}
        enemy_name = choice(enemies)
        enemy['model'] = "tower_app.enemy"
        enemy["pk"] = i
        enemy["fields"] = {
            # 'id' : 1,
            'enemy_name': enemy_name,
            'strength': randint(1, 15),
            'hp': randint(1, 15),
            'description': f"{enemy_name} fights",
            'roomID': randint(start, start + 10)
        }
        # print(e)
        e.append(enemy)
    return e

# floor 1 = 1 + 10 * 0
# floor 2 = 2 + 10 * 1
# floor 3 = 3 + 10 * 2


def floor_spawn(enemies):
    floor_num = 1
    total_enemies = []

    while floor_num <= 10:
        floor_enemies = enemy_gen(enemies, floor_num)
        total_enemies = total_enemies + floor_enemies
        floor_num = floor_num + 1
    return total_enemies


with open('../tower_app/fixtures/enemies_fixture.json', 'w') as file:
    json.dump(floor_spawn(enemies), file, indent=2)