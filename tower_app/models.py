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
        items = Item.objects.filter(roomID=self.id)
        # return [i.item_name for i in items]
        return items

    def __str__(self):
        return self.room_name


class Player(models.Model):
    # uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=64,
                            default=f"Room {random.choice(string.ascii_letters)}")  # attempting to generate a random room name using ascii_letters from string library and random.choice()
    hp = models.IntegerField(default=10)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)

    # default=Room.objects.get(room_name='Outside')
    # inventory = models.ForeignKey(Inventory)

    def inventory(self):
        inventory = Item.objects.filter(playerID=self.id)
        return [i.item_name for i in inventory]

    def pickup(self, item_name):
        items = Item.objects.filter(item_name=item_name, roomID=self.room.id)

        if items:
            item = items[0]
            item.roomID = 0
            item.playerID = self.id
            item.save()
            return f'{self.name} picked up the {item} from {self.room}'

        return f"{item} is not in the room. can't pick it up."

    def drop(self, item_name):
        items = Item.objects.filter(item_name=item_name, playerID=self.id)

        if items:
            item = items[0]
            item.roomID = self.room.id
            item.playerID = 0
            item.save()
            return f'{self.name} dropped the {item} in {self.room}'

        return f"{item} is not in your inventory. You can't drop it."

    def initialize(self):
        # start = input(f"{self.name}, you are outside the PyTower. It is a 10 story tower. There is a treasure chest
        # on the top floor. Do you have what it takes to reach the top??? type 'y' to enter Pytower: ")
        self.room = Room.objects.get(room_name='Outside')
        return self.room

    def move(self, way=""):
        if self.room.left == 'Staircase' or self.room.right == 'Staircase' or self.room.up == 'Staircase' or self.room.down == 'Staircase':
            stair = Room.objects.get(room_name='Staircase', floor=self.room.floor)
            self.room = Room.objects.get(id=stair.id + 1)
            room_enemies = Enemy.objects.filter(roomID=self.room.id)
            for enemy in room_enemies:
                enemy.enemy_strikes_player(self)
            return f'Congratulations, {self.name} has moved to floor {self.room.floor}. Now in {self.room.room_name} Room.'

        if way == 'up':
            if not self.room.up:
                return 'you cannot go that way. no rooms there...'
            else:
                self.room = Room.objects.get(room_name=self.room.up)
                print('in room: ', self.room, 'up:', self.room.up, 'down:', self.room.down, 'left:', self.room.left,
                      'right:', self.room.right)
                room_enemies = Enemy.objects.filter(roomID=self.room.id)
                for enemy in room_enemies:
                    enemy.enemy_strikes_player(self)
                return self.room

        elif way == 'down':
            if not self.room.down:
                return 'you cannot go that way. no rooms there...'
            else:
                # if self.room.down == 'Staircase':
                #     self.room = Room.objects.get(id = 11)
                # else:
                self.room = Room.objects.get(room_name=self.room.down)
                print('in room: ', self.room, 'up:', self.room.up, 'down:', self.room.down, 'left:', self.room.left,
                      'right:', self.room.right)
                room_enemies = Enemy.objects.filter(roomID=self.room.id)
                for enemy in room_enemies:
                    enemy.enemy_strikes_player(self)
                return self.room

        elif way == 'left':
            if not self.room.left:
                return 'you cannot go that way. no rooms there...'
            else:
                self.room = Room.objects.get(room_name=self.room.left)
                print('in room-', self.room, 'up-', self.room.up, 'down-', self.room.down, 'left-', self.room.left,
                      'right-', self.room.right)
                room_enemies = Enemy.objects.filter(roomID=self.room.id)
                for enemy in room_enemies:
                    enemy.enemy_strikes_player(self)
                return self.room

        elif way == 'right':
            if not self.room.right:
                return 'you cannot go that way. no rooms there...'
            else:
                self.room = Room.objects.get(room_name=self.room.right)
                print('in room: ', self.room, 'up:', self.room.up, 'down:', self.room.down, 'left:', self.room.left,
                      'right:', self.room.right)
                room_enemies = Enemy.objects.filter(roomID=self.room.id)
                for enemy in room_enemies:
                    enemy.enemy_strikes_player(self)
                return self.room
        else:
            return 'you have entered an invalid direction'

    def __str__(self):
        if not self.room:
            return f"{self.name} is outside."
        else:
            return f"{self.name} in {self.room}"


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
    # def random_string(self):
    #     return str(randint(1, 21))

    enemy_name = models.CharField(max_length=64)
    # # room = models.ForeignKey(Room,
    #                          on_delete=models.CASCADE,
    #                          blank=True,
    #                          null=True)
    # enemy_type = models.CharField(max_length=64)
    roomID = models.IntegerField(default=random.randint(1, 110))
    hp = models.IntegerField(default=random.randint(1, 15))
    strength = models.IntegerField(default=random.randint(1, 15))
    description = models.CharField(max_length=500, default='enemy description')

    # def spawn_enemies(self):
    #
    #     rooms = Room.objects.all()
    #     room_1 = choice(rooms)
    #     room_2 = choice(rooms)
    #     enemy_1 = choice(self.enemy_list)
    #     enemy_2 = choice(self.enemy_list)
    #
    #     spawn_enemy1 = Enemy(name=enemy_1)
    #     spawn_enemy2 = Enemy(name=enemy_2)
    #
    #     spawn_enemy1.save()
    #     spawn_enemy2.save()
    #
    #     spawn_enemy1.location = room_1.id
    #     spawn_enemy2.location = room_2.id
    #
    #     spawn_enemy1.save()
    #     spawn_enemy2.save()
    #     # spawned_enemies = sample(self.enemy_list, 2)
    #     # spawned_enemies[0] = choice(self.location)
    #     # spawned_enemies[1] = choice(self.location)
    #
    #     #     return f'{self.name}, Beware of your enemies!, {self.location.room_name}'
    #     # else:
    #     #     return f'{self.name}, Are you afraid to fight?'

    def enemy_strikes_player(self, player):
        player_room = player.room.id
        # enemies_in_room = Enemy.objects.filter(roomID=player_room)
        # if len(enemies_in_room) > 0:
        #     # sleep(5)
        #     for enemy in enemies_in_room:
        player.hp = player.hp - self.strength
        player.save()
        if player.hp <= 0:
            player.initialize()
            player.save()
            return f'{player.name}, Oh no! You have been slayed. Please try again from the beginning.'
        return f'{player.name}, You have been hit and now your HP is {player.hp}'

    def player_strikes_enemy(self, player):
        # player_room = player.room.id
        # enemies_in_room = Enemy.objects.filter(roomID=player_room)
        # if len(enemies_in_room) > 0:
        self.hp = self.hp - player.strength

        if self.hp <= 0:
            self.delete()
            return f'{player.name}, Victory! You have slayed {self.enemy_name}!'
        return f"{player.name}, You have hit {self.enemy_name} and now {self.enemy_name}'s HP is {self.hp}"
