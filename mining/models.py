from django.db import models
from django.contrib.auth.models import User

EXPLOSION = 0
SPACE = 1
ORE = 2

class Red(models.Model):
    FACES = [EXPLOSION, EXPLOSION, EXPLOSION, SPACE, SPACE, ORE]

class Yellow(models.Model):
    FACES = [EXPLOSION, EXPLOSION, SPACE, SPACE, ORE, ORE]

class Green(models.Model):
    FACES = [EXPLOSION, SPACE, SPACE, ORE, ORE, ORE]

class Game(models.Model):
    DICE = [Green()] * 6 + [Yellow()] * 4 + [Red()] * 3
    players = models.ManyToManyField(User)
    turn = models.ForeignKey(User, related_name='turn')

class Score(models.Model):
    game = models.ForeignKey(Game)
    player = models.ForeignKey(User)
    score = models.PositiveIntegerField()
