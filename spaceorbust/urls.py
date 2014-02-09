from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'spaceorbust.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^launch/', include('launch.urls', namespace='launch')),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^admin/', include(admin.site.urls)),
)
