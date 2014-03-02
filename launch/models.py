from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    clocks = models.IntegerField(default=8)
    fuses = models.IntegerField(default=3)
    drawpile = models.ForeignKey('Hand', related_name='drawpile', null=True)
    discardpile = models.ForeignKey('Hand', related_name='discardpile', null=True)
    launchpad = models.ForeignKey('Hand', related_name='launchpad', null=True)
    ispublic = models.BooleanField(default=True)
    players = models.ManyToManyField(User)

    
class Hand(models.Model):
    """Represents a player hand of cards.  Hand is loosely defined here, the
    draw pile, discard pile, and launch pad also count as 'hands'."""
    def isvisible(self, player):
        """Is this hand visible to the specified player?"""
        return (self.player is None) or (self.player != player)
    
    player = models.ForeignKey(User, null=True)
    game = models.ForeignKey(Game)


class Card(models.Model):
    COMMAND = 'CM'
    LIFESUPPORT = 'LS'
    SENSORS = 'SN'
    FUELTANKS = 'FT'
    ENGINES = 'EN'
    suits = ((COMMAND, 'Command Module'),
             (LIFESUPPORT, 'Life Support'),
             (SENSORS, 'Sensors'),
             (FUELTANKS, 'Fuel Tanks'),
             (ENGINES, 'Engines'))
    suit = models.CharField(max_length=2, choices=suits)
    number = models.IntegerField(default=1)
    hand = models.ForeignKey(Hand)


class Note(models.Model):
    """Players can take notes on a card."""
    text = models.TextField()
    card = models.ForeignKey(Card)
    user = models.ForeignKey(User)
