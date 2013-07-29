from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


# enable databrowse
from django.contrib import databrowse
from medline.models import *

databrowse.site.register( Meshterm )
databrowse.site.register( Branch )
databrowse.site.register( Subheading )
databrowse.site.register( Meshcitation )
databrowse.site.register( Subheadingterm )
databrowse.site.register( Journal )
databrowse.site.register( Organization )
databrowse.site.register( PubType )
databrowse.site.register( Author )
databrowse.site.register( Language )
databrowse.site.register( Citation )


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'meddle.views.home', name='home'),
    # url(r'^meddle/', include('meddle.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin: 
    url(r'^admin/', include(admin.site.urls)),

    url(r'^databrowse/(.*)', databrowse.site.root),                       
)
