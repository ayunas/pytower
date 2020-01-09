from django.db import models
import string,random
# import uuid
# from django.db import models
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from rest_framework.authtoken.models import Token


class Room(models.Model):
        ### Field Columns in Room Table ###
    room_name = models.CharField(max_length = 64)
    description = models.CharField(max_length=500, default=f"No Room description'" )
    up = models.CharField(max_length = 64, default="")
    down = models.CharField(max_length = 64, default="")
    left = models.CharField(max_length = 64, default="")
    right = models.CharField(max_length = 64, default="")

    def items(self):
        items = Item.objects.filter(roomID = self.id)
        return [i.item_name for i in items]

    def __str__(self):
        return self.room_name

class Player(models.Model):
    # uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    HP = models.IntegerField(default=10)
    name = models.CharField(max_length=64, default=f"Room {random.choice(string.ascii_letters)}")#attempting to generate a random room name using ascii_letters from string library and random.choice()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    # inventory = models.ForeignKey(Inventory)
    
    def inventory(self):
        inventory = Item.objects.filter(playerID = self.room.id)
        return [i.item_name for i in inventory]

    # def pickup(self,item):
    #     print(self.room.id)
    #     room_items = Item.objects.filter(roomID = self.room.id)
    #     items = [ri.item_name for ri in room_items]
        
    #     if item in items:
    #         i = Item.objects.filter(item_name = item)
    #         i[0].roomID = 0
    #         i[0].playerID = self.id
    #         i[0].save()
    #         i[0].persist()
    #         return f'{self.name} picked up the {item} from {self.room}'
    #     else:
    #         return f"{item} is not in the room. can't pick it up."

    def pickup(self, item_name):
        items = Item.objects.filter(item_name=item_name, roomID=self.room.id)

        if items:
            item = items[0]
            item.roomID = 0
            item.playerID = self.id
            item.save()
            return f'{self.name} picked up the {item} from {self.room}'

        return f"{item} is not in the room. can't pick it up."
        
    def drop_item(self,item):
        pass

    def initialize(self,start):
        # start = input(f"{self.name}, you are outside the PyTower. It is a 10 story tower. There is a treasure chest on the top floor. Do you have what it takes to reach the top??? type 'y' to enter Pytower: ")

        if start == 'y':
            self.room = Room.objects.get(room_name = "Foyer")
            print(f"{self.name}, you have now entered the {self.room.room_name}")
            return f"{self.name}, you have now entered the {self.room.room_name}"
        else:
            print(f"{self.name}, when you're ready for Pytower, you may enter!")
            return f"{self.name}, when you're ready for Pytower, you may enter!"

        print(self.room.description)
        print('in room: ', self.room, 'up:',self.room.up, 'down:',self.room.down, 'left:',self.room.left, 'right:', self.room.right)
        return self.room
            
    def move(self,way=""):
        # print(self.room[way])  #causes error, Room object not subscriptable
        # print(way)
        # if self.room[way]:
        #     pass
        if way == 'up':
            if not self.room.up:
                print('you cannot go that way. no rooms there...')
                return 'you cannot go that way. no rooms there...'
            else:
                self.room = Room.objects.get(room_name = self.room.up)
                print('in room: ', self.room, 'up:',self.room.up, 'down:',self.room.down, 'left:',self.room.left, 'right:', self.room.right)
                return self.room

        elif way == 'down':
            if not self.room.down:
                print('you cannot go that way. no rooms there...')
                return 'you cannot go that way. no rooms there...'
            else:
                self.room = Room.objects.get(room_name = self.room.down)
                print('in room: ', self.room, 'up:',self.room.up, 'down:',self.room.down, 'left:',self.room.left, 'right:', self.room.right)
                return self.room

        elif way == 'left':
            if not self.room.left:
                print('you cannot go that way. no rooms there...')
                return 'you cannot go that way. no rooms there...'
            else:
                self.room = Room.objects.get(room_name = self.room.left)
                print('in room-', self.room, 'up-',self.room.up, 'down-',self.room.down, 'left-',self.room.left, 'right-', self.room.right)
                return self.room
        
        elif way == 'right':
            if not self.room.right:
                print('you cannot go that way. no rooms there...')
                return 'you cannot go that way. no rooms there...'
            else:
                self.room = Room.objects.get(room_name = self.room.right)
                print('in room: ', self.room, 'up:',self.room.up, 'down:',self.room.down, 'left:',self.room.left, 'right:', self.room.right)
                return self.room
            
        else:
            print('you have entered an invalid direction')
            return 'you have entered an invalid direction'

    def __str__(self):
        if not self.room:
            return  f"{self.name} is outside." 
        else:
            return f"{self.name} in {self.room}"

class Item(models.Model):
    item_name = models.CharField(max_length=64)
    strength = models.IntegerField(default=5)
    item_type = models.CharField(max_length=64,default="weapon")
    # playerID = models.ForeignKey(Player, on_delete=models.CASCADE, null=True)
    # roomID = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    playerID = models.IntegerField(blank=True,null=True)
    roomID = models.IntegerField(default=1,null=True,blank=True)

    def persist(self):
        self.save()

    def __str__(self):
        return self.item_name

class Floor(models.Model):
    pass

