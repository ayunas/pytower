from django.db import models

class Room(models.Model):
    room = models.CharField(max_length = 64)

    def __str__(self):
        return f"{self.room}"

class Player(models.Model):
    name = models.CharField(max_length=64)
    location = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True)

    def move(self):
       pass
    
    def __str__(self):
        return f"{self.name} in {self.location}" 




