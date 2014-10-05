from django.http import HttpResponse
from django.shortcuts import render

from mining.models import Game


def index(request):
    return HttpResponse('hello world')

def game(request, pk):
    g = Game.objects.get(pk=pk)
    return render(request, 'mining/game.html', {'game': g})