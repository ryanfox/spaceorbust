from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic

from launch.forms import *
from launch.models import *


def index(request):
    return HttpResponse('Hello, world')

def game(request, pk):
    g = get_object_or_404(Game, pk=pk)
    if request.method == 'POST':
        form = InviteForm(request.POST)
        if form.is_valid():
            u = get_object_or_404(User, username=form.cleaned_data['username'])
            import pdb;pdb.set_trace()
            if u is not None and not u in g.players.all():
                g.players.add(u)
                g.save()
                
                h = Hand()
                h.game = g
                h.player = u
                h.save()
    else:
        form = InviteForm()
        
    context = {'game': g}
    context['form'] = form
    context['commandmodule'] = g.launchpad.card_set.filter(suit=Card.COMMAND).count()
    context['lifesupport'] = g.launchpad.card_set.filter(suit=Card.LIFESUPPORT).count()
    context['sensors'] = g.launchpad.card_set.filter(suit=Card.SENSORS).count()
    context['fueltanks'] = g.launchpad.card_set.filter(suit=Card.FUELTANKS).count()
    context['engines'] = g.launchpad.card_set.filter(suit=Card.ENGINES).count()
    
    context['hands'] = [hand for hand in g.hand_set.exclude(player=None).exclude(player=request.user)]
    return render(request, 'launch/game.html', context)

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
    """Create a new game.  Initially only has one player."""
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

    return HttpResponseRedirect(reverse('launch:game', args=(g.id,)))

@login_required
def deal(request, pk):
    """Deal 5 cards to each player in the game."""
    game = get_object_or_404(Game, pk=pk)
    if game.turn == None:
        for player in game.players.all():
            cards = game.drawpile.card_set.all().order_by('?')[:5]
            for card in cards:
                card.hand = game.hand_set.filter(player=player).get()
                card.save()

        game.turn = game.players.all().order_by('?')[0]
        game.save()
    return HttpResponseRedirect(reverse('launch:game', args=(game.id,)))
