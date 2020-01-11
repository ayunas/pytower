from django.db import models
import string, random


class Room(models.Model):
    ### Field Columns in Room Table ###
    room_name = models.CharField(max_length=64)
    description = models.CharField(max_length=500, default=f"No Room description'")
    up = models.CharField(max_length=64, default="")
    down = models.CharField(max_length=64, default="")
    left = models.CharField(max_length=64, default="")
    right = models.CharField(max_length=64, default="")
    floor = models.IntegerField(default=1)

    def items(self):
        items = Item.objects.filter(roomID=self.id, playerID__isnull=True)
        # return [i.item_name for i in items]
        return list(items)

    def enemies(self):
        # enemies = Enemy.objects.filter(roomID__gte=1, roomID__lte=11)
        enemies = Enemy.objects.filter(roomID = self.id)
        
        return enemies
    
    def mapping(self):
        mapping = {'current room' : self.room_name, 'up' : None if not self.up else self.up,
        'down' : None if not self.down else self.down,
        'left' : None if not self.left else self.left,
        'right' : None if not self.right else self.right,
        }
        return mapping

    def __str__(self):
        return self.room_name

class Player(models.Model):
    # uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=64,
                            default=f"Room {random.choice(string.ascii_letters)}")  # attempting to generate a random room name using ascii_letters from string library and random.choice()
    hp = models.IntegerField(default=10)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    strength = models.IntegerField(default=random.randint(1, 30))

    # default=Room.objects.get(room_name='Outside')
    # inventory = models.ForeignKey(Inventory)

    def inventory(self):
        inventory = Item.objects.filter(playerID = self.id)
        return inventory

    def pickup(self, item_name):
        items = Item.objects.filter(item_name=item_name, roomID=self.room.id)
        if items:
            item = items[0]
            item.roomID = 0
            item.playerID = self.id
            if item.item_type == 'armor':
                self.hp = self.hp + item.strength
                item.save()
                self.save()
                return f'{self.name} picked up the {item} from {self.room}. Increased HP: {self.hp}'
            if item.item_type == 'weapon':
                self.strength = self.strength + item.strength
                item.save()
                self.save()
                return f'{self.name} picked up the {item} from {self.room}. Increased strength: {self.strength}'

            
        
            return f'{self.name} picked up the {item} from {self.room}. Increased HP: {self.hp}'

        return f"{item_name} is not in the room. can't pick it up."

    def drop(self, item_name):
        items = Item.objects.filter(item_name=item_name, playerID=self.id)

        if items:
            item = items[0]
            if item.item_type == 'weapon':
                self.strength = self.strength - item.strength
            if item.item_type == 'armor':
                if self.hp - item.strength <= 0:
                    return f"cannot drop {item.item_name}. You're HP is only {self.hp}."
                self.hp = self.hp - item.strength
            item.roomID = self.room.id
            item.playerID = None
            item.save()
            self.save()
            return f'{self.name} dropped the {item} in {self.room}.  reduced HP : {self.hp}'

        return f"{item_name} is not in your inventory. You can't drop it."

    def initialize(self):
        # start = input(f"{self.name}, you are outside the PyTower. It is a 10 story tower. There is a treasure chest
        # on the top floor. Do you have what it takes to reach the top??? type 'y' to enter Pytower: ")
        inventory = Item.objects.filter(playerID = self.id)
        for item in inventory:
            item.playerID = 0
            item.save()
        self.room = Room.objects.get(room_name='Outside')
        self.hp = random.randint(10,30)
        return {'player':self.name, 'HP':self.hp, 'strength':self.strength, 'room':self.room.room_name}

    def enemy_attack(self, message=None):
        room_enemies = Enemy.objects.filter(roomID=self.room.id)
        for enemy in room_enemies:
            strike = random.randint(0,1)
            if strike:
                if message is None:
                    message=f"\n{enemy.enemy_name} is attacking you!"
                else:
                    message=message + f"\n{enemy.enemy_name} is attacking you!"
                attack_message = enemy.enemy_strikes_player(self)
                message=message + attack_message
        return message

    def move(self, way=""):
        
        if self.room.left == 'Staircase' and way=="left" or self.room.right == 'Staircase' and way =="right" or self.room.up == 'Staircase' and way=="up" or self.room.down == 'Staircase' and way=="down":
            stair = Room.objects.get(room_name='Staircase', floor=self.room.floor)
            self.room = Room.objects.get(id=stair.id + 1)
            self.hp = self.hp + 10*self.room.floor
            self.save()
            message=f'Congratulations, {self.name} has moved to floor {self.room.floor}. {self.name} HP increased to {self.hp}.  Now in {self.room.room_name} Room.'
            # room_enemies = Enemy.objects.filter(roomID=self.room.id)
            # for enemy in room_enemies:
            #     strike = random.randint(0,1)
            #     if strike:
            #         message=message + f"{enemy.enemy_name} is attacking you!"
            #         enemy.enemy_strikes_player(self)
            message = self.enemy_attack(message)
        
            return message

        if way == 'up':
            if not self.room.up:
                return 'you cannot go that way. no rooms there...'
            else:
                self.room = Room.objects.get(room_name=self.room.up)
                self.save()
                # print('in room: ', self.room, 'up:', self.room.up, 'down:', self.room.down, 'left:', self.room.left,
                #       'right:', self.room.right)
                # room_enemies = Enemy.objects.filter(roomID=self.room.id)
                # for enemy in room_enemies:
                #     strike = random.randint(0,1)
                #     if strike:
                #         message = f"{enemy.enemy_name} is attacking you!"
                #         enemy.enemy_strikes_player(self)
                #         return message
                # print('PLAYER NEW room ',self.room)
                message= self.enemy_attack()
                return message

        elif way == 'down':
            if not self.room.down:
                return 'you cannot go that way. no rooms there...'
            else:
                # if self.room.down == 'Staircase':
                #     self.room = Room.objects.get(id = 11)
                # else:
                self.room = Room.objects.get(room_name=self.room.down)
                self.save()
                self.room.mapping()
                # print('in room: ', self.room, 'up:', self.room.up, 'down:', self.room.down, 'left:', self.room.left,
                #       'right:', self.room.right)
                # room_enemies = Enemy.objects.filter(roomID=self.room.id)
                # for enemy in room_enemies:
                #     strike = random.randint(0,1)
                #     if strike:
                #         message=f"{enemy.enemy_name} is attacking you!"
                #         enemy.enemy_strikes_player(self)
                #         return message
                # print('room items',self.room.items())
                message = self.enemy_attack()
                return message

        elif way == 'left':
            if not self.room.left:
                return 'you cannot go that way. no rooms there...'
            else:
                self.room = Room.objects.get(room_name=self.room.left)
                self.save()
                self.room.mapping()
                # room_enemies = Enemy.objects.filter(roomID=self.room.id)
                # for enemy in room_enemies:
                #     strike = random.randint(0,1)
                #     if strike:
                #         message=f"{enemy.enemy_name} is attacking you!"
                #         enemy.enemy_strikes_player(self)
                #         return message
                # print('room items',self.room.items())
                message= self.enemy_attack()
                return message

        elif way == 'right':
            if not self.room.right:
                return 'you cannot go that way. no rooms there...'
            else:
                self.room = Room.objects.get(room_name=self.room.right)
                self.save()
                self.room.mapping()
                # room_enemies = Enemy.objects.filter(roomID=self.room.id)
                # for enemy in room_enemies:
                #     strike = random.randint(0,1)
                #     if strike:
                #         print(f"{enemy.enemy_name} is attacking you!")
                #         enemy.enemy_strikes_player(self)
                # print('room items',self.room.items())
                message = self.enemy_attack()
                return message
        else:
            return 'you have entered an invalid direction'

    def __str__(self):
        # if not self.room:
        #     return f"{self.name} is outside."
        # else:
        return self.name


class Item(models.Model):
    item_name = models.CharField(max_length=64)
    strength = models.IntegerField(default=5)
    item_type = models.CharField(max_length=64, default="weapon")
    description = models.CharField(max_length=256, default="Item Description")
    playerID = models.IntegerField(blank=True, null=True)
    roomID = models.IntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return self.item_name


class Enemy(models.Model):
 
    enemy_name = models.CharField(max_length=64)
    # # room = models.ForeignKey(Room,on_delete=models.CASCADE,blank=True,null=True)
    roomID = models.IntegerField(default=random.randint(1, 110))
    hp = models.IntegerField(default=random.randint(1, 15))
    strength = models.IntegerField(default=random.randint(1, 15))
    description = models.CharField(max_length=500, default='enemy description')

    def __str__(self):
        return self.enemy_name

    def enemy_strikes_player(self, player):
        
        player_room = player.room.id
        print(f'{player.name} HP: {player.hp}, {self.enemy_name} strength: {self.strength}')
        player.hp = player.hp - self.strength
        player.save()
        if player.hp <= 0:
            player.initialize()
            player.save()
            return f'{player.name}, Oh no! You have been slayed. Please try again from the beginning.'
        print(f'{player.name}, You have been hit and now your HP is {player.hp}')
        return f'{player.name}, You have been hit and now your HP is {player.hp}'

    def player_strikes_enemy(self, player):
        print("PLAYER STRIKING ENEMY")
        # player_room = player.room.id
        # enemies_in_room = Enemy.objects.filter(roomID=player_room)
        # if len(enemies_in_room) > 0:
        self.hp = self.hp - player.strength
        self.save()
        if self.hp <= 0:
            self.delete()
            return f'{player.name}, Victory! You have slayed {self.enemy_name}!'
        return f"{player.name}, You have hit {self.enemy_name} and now {self.enemy_name}'s HP is {self.hp}"
