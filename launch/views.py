from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic

from launch.models import *


def index(request):
    return HttpResponse('Hello, world')

class GameView(generic.DetailView):
    model = Game
    template_name = 'launch/game.html'

def initializedeck(drawpile):
    """Initialize a deck.  All cards start in the draw pile initially."""
    for suit in Card.suits:
        createcard(suit[0], 1, drawpile)
        createcard(suit[0], 1, drawpile)
        createcard(suit[0], 1, drawpile)
        createcard(suit[0], 2, drawpile)
        createcard(suit[0], 2, drawpile)
        createcard(suit[0], 3, drawpile)
        createcard(suit[0], 3, drawpile)
        createcard(suit[0], 4, drawpile)
        createcard(suit[0], 4, drawpile)
        createcard(suit[0], 5, drawpile)

def createcard(suit, number, hand):
    """Create a card belonging to the specified hand, with given suit and value."""
    c = Card()
    c.suit = suit
    c.number = number
    c.hand = hand
    c.save()

@login_required
def create(request):
    g = Game()
    g.save()

    drawpile = Hand()
    drawpile.game = g
    drawpile.save()
    initializedeck(drawpile)
    
    discardpile = Hand()
    discardpile.game = g
    discardpile.save()
    
    launchpad = Hand()
    launchpad.game = g
    launchpad.save()

    g.drawpile = drawpile
    g.discardpile = discardpile
    g.launchpad = launchpad
    g.players.add(request.user)
    g.save()
    return HttpResponseRedirect(reverse('launch:game', args=(g.id,)))
