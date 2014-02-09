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

@login_required
def create(request):
    g = Game()
    g.save()

    drawpile = Hand()
    drawpile.game = g
    drawpile.save()
    
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
