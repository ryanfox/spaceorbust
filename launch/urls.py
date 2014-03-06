from django.conf.urls import patterns, url

from launch import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^g/(?P<pk>\d+)/$', views.game, name='game'),
    url(r'^g/create/$', views.create, name='create'),
    url(r'^g/(?P<pk>\d+)/deal/$', views.deal, name='deal'),
    url(r'^u/(?P<pk>\d+)/$', views.user, name='user'),
    url(r'^i/(?P<pk>\d+)/accept/$', views.accept, name='accept'),
    url(r'^i/(?P<pk>\d+)/decline/$', views.decline, name='decline'),
)
