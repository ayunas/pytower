import json, random, requests

weapons = ['scimitar', 'short sword', 'crystal sword', 'falchion', 'war sword', 'broad sword', 'dimensional blade',
           'ancient sword', 'Bronze Axe', 'Bows', 'Crossbows', 'Gold Dagger', 'Wooken Javelin', 'Silver Mace',
           'Executioner Sword', 'Polearm', 'Scepter', 'Piercing Spear', 'Stave', 'Mystifying Wand']

armors = ['chain mail', 'quilted armor', 'leather armor', 'studded leather', 'ring mail', 'breast plate', 'splint mail',
          'full plate mail', 'buckler', 'small shield', 'bone shield', 'kite shield', 'gothic shield', 'ancient armor']


def weapongen(weapons):
    w = []
    for i in range(50):
        weapon = {}
        weapon_name = random.choice(weapons)
        weapon['model'] = "tower_app.item"
        weapon["pk"] = i + 1
        weapon["fields"] = {
            # 'id' : 1,
            'item_name': weapon_name,
            'strength': random.randint(1, 10),
            'item_type': 'weapon',
            'description': f"{weapon_name} attacks",
            'playerID': None,
            'roomID': random.randint(1, 110)
        }
        w.append(weapon)
    return w


def armorgen(armors):
    i = 51
    a = []
    while i < 100:
        armor = {}
        armor_name = random.choice(armors)
        armor['model'] = "tower_app.item"
        armor["pk"] = i
        armor["fields"] = {
            # 'id' : 1,
            'item_name': armor_name,
            'strength': random.randint(1, 10),
            'item_type': 'armor',
            'description': f"{armor_name} protects",
            'playerID': None,
            'roomID': random.randint(1, 110)
        }
        a.append(armor)
        i = i + 1
    return a


with open('./fixtures/weapon_fixture.json', 'w') as file:
    json.dump(weapongen(weapons), file, indent=2)

with open('./fixtures/armor_fixture.json', 'w') as file:
    json.dump(armorgen(armors), file, indent=2)
