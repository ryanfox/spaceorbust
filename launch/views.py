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

    def get_context_data(self, **kwargs):
        context = super(GameView, self).get_context_data(**kwargs)
        context['commandmodule'] = self.object.launchpad.card_set.filter(suit=Card.COMMAND).count()
        context['lifesupport'] = self.object.launchpad.card_set.filter(suit=Card.LIFESUPPORT).count()
        context['sensors'] = self.object.launchpad.card_set.filter(suit=Card.SENSORS).count()
        context['fueltanks'] = self.object.launchpad.card_set.filter(suit=Card.FUELTANKS).count()
        context['engines'] = self.object.launchpad.card_set.filter(suit=Card.ENGINES).count()
        
        for hand in self.object.hand_set.exclude(player=None).exclude(player=self.request.user):
            context[hand.player.username] = hand.card_set.all()
        
        return context

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

def deal(game):
    """Deal 5 cards to each player in the game."""
    for player in game.players.all():
        cards = game.drawpile.card_set.all().order_by('?')[:5]
        for card in cards:
            card.hand = game.hand_set.filter(player=player).get()
            card.save()

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
    
    h = Hand()
    h.player = request.user
    h.game = g
    h.save()

    deal(g)
    return HttpResponseRedirect(reverse('launch:game', args=(g.id,)))
