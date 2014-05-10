from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from django.contrib import admin
admin.autodiscover()

from .sitemap import sitemaps

urlpatterns = patterns('',
	url(r'^$', RedirectView.as_view(url='/blog/')),
    url(r'^{}/'.format(settings.ADMIN_URL), include(admin.site.urls)),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^landing/', include('landing.urls', namespace='landing')),
    url(r'^projects/', include('projects.urls', namespace='projects')),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps})

)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
