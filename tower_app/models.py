from django.db import models
import string,random

class Room(models.Model):
        ### Field Columns in Room Table ###
    room_name = models.CharField(max_length = 64)
    description = models.CharField(max_length=500, default=f"No Room description'" )
    up = models.CharField(max_length = 64, default="")
    down = models.CharField(max_length = 64, default="")
    left = models.CharField(max_length = 64, default="")
    right = models.CharField(max_length = 64, default="")
    floor = models.IntegerField(default=1)

    def items(self):
        items = Item.objects.filter(roomID = self.id)
        return [i.item_name for i in items]

    def __str__(self):
        return self.room_name

class Player(models.Model):
    # uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    hp = models.IntegerField(default=10)
    name = models.CharField(max_length=64, default=f"Room {random.choice(string.ascii_letters)}")#attempting to generate a random room name using ascii_letters from string library and random.choice()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    # default=Room.objects.get(room_name='Outside')
    # inventory = models.ForeignKey(Inventory)
    
    def inventory(self):
        inventory = Item.objects.filter(playerID = self.id)
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
        
    def drop(self,item_name):
        items = Item.objects.filter(item_name = item_name, playerID=self.id)
        
        if items:
            item = items[0]
            item.roomID = self.room.id
            item.playerID = 0
            item.save()
            return f'{self.name} dropped the {item} in {self.room}'
        
        return f"{item} is not in your inventory. You can't drop it."

    def initialize(self):
        # start = input(f"{self.name}, you are outside the PyTower. It is a 10 story tower. There is a treasure chest on the top floor. Do you have what it takes to reach the top??? type 'y' to enter Pytower: ")
        self.room = Room.objects.get(room_name = 'Outside')
        return self.room
            
    def move(self,way=""):
      
        if way == 'up':
            if not self.room.up:
                return 'you cannot go that way. no rooms there...'
            else:
                self.room = Room.objects.get(room_name = self.room.up)
                self.save()
                print('in room: ', self.room, 'up:',self.room.up, 'down:',self.room.down, 'left:',self.room.left, 'right:', self.room.right)
                return

        elif way == 'down':
            if not self.room.down:
                return 'you cannot go that way. no rooms there...'
            else:
                self.room = Room.objects.get(room_name = self.room.down)
                self.save()
                print('in room: ', self.room, 'up:',self.room.up, 'down:',self.room.down, 'left:',self.room.left, 'right:', self.room.right)
                return 

        elif way == 'left':
            if not self.room.left:
                return 'you cannot go that way. no rooms there...'
            else:
                self.room = Room.objects.get(room_name = self.room.left)
                self.save()
                print('in room-', self.room, 'up-',self.room.up, 'down-',self.room.down, 'left-',self.room.left, 'right-', self.room.right)
                return 
        
        elif way == 'right':
            if not self.room.right:
                return 'you cannot go that way. no rooms there...'
            else:
                self.room = Room.objects.get(room_name = self.room.right)
                self.save()
                print('in room: ', self.room, 'up:',self.room.up, 'down:',self.room.down, 'left:',self.room.left, 'right:', self.room.right)
                return self.room
        else:
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

    def __str__(self):
        return self.item_name

class Floor(models.Model):
    pass

