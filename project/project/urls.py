from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
admin.autodiscover()

from subdomains.views import create_subdomain
from .views import subdomainform

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^project/', include('project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', subdomainform, name='index'),
    url(r'^submit/', create_subdomain, name='subdomains_create_subdomain'),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)