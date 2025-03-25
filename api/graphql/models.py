from django.db import models

class Game(models.Model):
    name =models.CharField(max_length=100)

class Player(models.Model):
    name= models.CharField(max_length=100)
    game = models.ForeignKey(Game,on_delete=nodels.CASCADE)
    joint_at = models.DateTimeField(auto_now_add=True)