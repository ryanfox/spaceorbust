from django.conf.urls import patterns, url

from mining import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^game/(?P<pk>\d+)$', views.game, name='game'),
)