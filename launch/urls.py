from django.conf.urls import patterns, url

from launch import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^g/(?P<pk>\d+)/$', views.game, name='game'),
    url(r'^g/create/$', views.create, name='create'),
    url(r'^g/?P<pk>(\d+)/deal/$', views.deal, name='deal'),
)
