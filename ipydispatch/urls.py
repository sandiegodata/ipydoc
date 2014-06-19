from django.conf.urls import patterns, url, include

from django.contrib import admin
admin.autodiscover()

from dispatcher.views import home, done, logout

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ipydispatch.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^done/$', done, name='done'),
    url(r'', include('social_auth.urls')),
    url(r'^logout/$', logout, name='logout'),
)
