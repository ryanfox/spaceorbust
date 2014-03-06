from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic

from launch.forms import *
from launch.models import *


def index(request):
    return HttpResponse('Hello, world. This is the launch index')

def game(request, pk):
    """Summary page for a game"""
    g = get_object_or_404(Game, pk=pk)
    if request.method == 'POST' and request.user.is_authenticated():
        form = InviteForm(request.POST)
        if form.is_valid() and g.players.count() < 5:
            u = get_object_or_404(User, username=form.cleaned_data['username'])
            if u is not None and not u in g.players.all():
                i = Invite()
                i.inviter = request.user
                i.invitee = u
                i.game = g
                i.status = Invite.PENDING
                i.save()
                
    # reset form
    form = InviteForm()
        
    context = {'game': g}
    context['form'] = form
    context['commandmodule'] = g.launchpad.card_set.filter(suit=Card.COMMAND).count()
    context['lifesupport'] = g.launchpad.card_set.filter(suit=Card.LIFESUPPORT).count()
    context['sensors'] = g.launchpad.card_set.filter(suit=Card.SENSORS).count()
    context['fueltanks'] = g.launchpad.card_set.filter(suit=Card.FUELTANKS).count()
    context['engines'] = g.launchpad.card_set.filter(suit=Card.ENGINES).count()
    
    hands = g.hand_set.exclude(player=None)
    if request.user.is_authenticated():
        hands = hands.exclude(player=request.user)
        context['turn'] = g.turn
        if g.turn == request.user:
            # TODO add hint, discard
            pass
    
    context['hands'] = hands
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
    g = get_object_or_404(Game, pk=pk)
    if g.turn == None:
        for player in g.players.all():
            cards = g.drawpile.card_set.all().order_by('?')[:5]
            for card in cards:
                card.hand = g.hand_set.filter(player=player).get()
                card.save()

        g.turn = g.players.all().order_by('?')[0]
        g.save()
    return HttpResponseRedirect(reverse('launch:game', args=(g.id,)))

def user(request, pk):
    """Get a user's summary page.  Show current games, completed games, scores,
    average score, average # players, etc.
    """
    u = get_object_or_404(User, pk=pk)
    context = {'user': u}
    if request.user.is_authenticated() and request.user.id == int(pk):
        context['invites'] = Invite.objects.filter(invitee=u).filter(status=Invite.PENDING)
    allgames = u.game_set.all()
    context['currentgames'] = [g for g in allgames if not g.isdone()]
    context['completedgames'] = [g for g in allgames if g.isdone()]
    return render(request, 'launch/user.html', context)

@login_required
def accept(request, pk):
    """Accept a game invite"""
    i = get_object_or_404(Invite, pk=pk)
    if i.invitee == request.user:
        i.status = Invite.ACCEPTED
        i.save()
        
        g = i.game
        g.players.add(request.user)
        g.save()
                
        h = Hand()
        h.game = g
        h.player = i.invitee
        h.save()
    return HttpResponseRedirect(reverse('launch:game', args=(i.game.id,)))

@login_required
def decline(request, pk):
    """Decline a game invite"""
    i = get_object_or_404(Invite, pk=pk)
    if i.invitee == request.user:
        i.status = Invite.REJECTED
        i.save()
    return HttpResponseRedirect(reverse('launch:user', args=(i.invitee.id,)))

@login_required
def givehint(request):
    """Give a player a hint about their cards."""
    raise NotImplementedError # TODO implement

@login_required
def discard(request):
    """Discard a card."""
    raise NotImplementedError # TODO implement

@login_required
def play(request):
    """Play a card."""
    raise NotImplementedError # TODO implement

