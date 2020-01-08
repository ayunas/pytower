from django.db import models
import string,random
import uuid

class Room(models.Model):
        ### Field Columns in Room Table ###
    room_name = models.CharField(max_length = 64)
    description = models.CharField(max_length=500, default=f"No Room description'" )
    up = models.CharField(max_length = 64, default="")
    down = models.CharField(max_length = 64, default="")
    left = models.CharField(max_length = 64, default="")
    right = models.CharField(max_length = 64, default="")

    # def connectRooms(self, room, direction):
    #     room_id = room.id
    #     try:
    #         room = Room.objects.get(id=room_id)
    #     except Room.DoesNotExist:
    #         print('That room does not exist')
    #     else:
    #         if direction == 'n':
    #             self.north = room_id
    #         elif direction == 's':
    #             self.south = room_id
    #         elif direction == 'e':
    #             self.east = room_id
    #         elif direction = 'w':
    #             self.west = room_id
    #         else:
    #             print("Invalid direction")
    #             return
    #         self.save()

    def __str__(self):
        return f"{self.room_name}"


class Player(models.Model):
    # uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=64, default=f"Room {random.choice(string.ascii_letters)}")#attempting to generate a random room name using ascii_letters from string library and random.choice()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, default=None, blank=True, null=True)

    def initialize(self):
        start = input(f"{self.name}, you are outside the PyTower. It is a 10 story tower. There is a treasure chest on the top floor. Do you have what it takes to reach the top??? type 'y' to enter Pytower: ")

        if start == 'y':
            self.room = Room.objects.get(room_name = "Foyer")
            print(f"{self.name}, you have now entered the {self.room.room_name}")
        else:
            print(f"{self.name}, when you're ready for Pytower, you may enter!")
            return

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
                return
            else:
                self.room = Room.objects.get(room_name = self.room.up)
                print('in room: ', self.room, 'up:',self.room.up, 'down:',self.room.down, 'left:',self.room.left, 'right:', self.room.right)
                return self.room

        elif way == 'down':
            if not self.room.down:
                print('you cannot go that way. no rooms there...')
                return
            else:
                self.room = Room.objects.get(room_name = self.room.down)
                print('in room: ', self.room, 'up:',self.room.up, 'down:',self.room.down, 'left:',self.room.left, 'right:', self.room.right)
                return self.room

        elif way == 'left':
            if not self.room.left:
                print('you cannot go that way. no rooms there...')
                return
            else:
                self.room = Room.objects.get(room_name = self.room.left)
                print('in room-', self.room, 'up-',self.room.up, 'down-',self.room.down, 'left-',self.room.left, 'right-', self.room.right)
                return self.room
        
        elif way == 'right':
            if not self.room.right:
                print('you cannot go that way. no rooms there...')
                return
            else:
                self.room = Room.objects.get(room_name = self.room.right)
                print('in room: ', self.room, 'up:',self.room.up, 'down:',self.room.down, 'left:',self.room.left, 'right:', self.room.right)
                return self.room
            
        else:
            print('you have entered an invalid direction')
            return

    def __str__(self):
        if not self.room:
            return  f"{self.name} is outside." 
        else:
            return f"{self.name} in {self.room}"


class Item(models.Model):
    item_name = models.CharField(max_length=64, )

class Floor(models.Model):
    pass

