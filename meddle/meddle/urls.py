from django.conf.urls import patterns, include, url
from meddle import settings
from medline import views
from medline.models import Citation
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from django_filters.views import FilterView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'meddle.views.home', name='home'),
    # url(r'^meddle/', include('meddle.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

   url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
           'document_root': settings.MEDIA_ROOT,
       }),
   url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
           'document_root': settings.STATIC_ROOT,
       }),                       

    # Uncomment the next line to enable the admin: 
    url(r'^admin/', include(admin.site.urls)),
    url(r'^htsql/', include('htsql_django.urls')),

    url(r'^citedin_trends/(?P<year>\d+)/$', views.cited_in_trends ),
    url(r'^citedin/(?P<year>\d+)/$', views.cited_in ),
    url(r'^mesh/(?P<year_start>\d+)/(?P<year_end>\d+)$', views.mesh_network ),
    url(r'^branches/(?P<year>\d+)/$', views.branch_network ),
    url(r'^jurisprudence/$', views.jurisprudence_network ),
    url(r'^breast_cancer/$', views.breast_cancer_network ),
    url(r'^clinical/$', views.clinical_network )                 
    url(r'^lista/', FilterView.as_view(model=Citation)),
    url(r'^list/', views.citation_list),
)
