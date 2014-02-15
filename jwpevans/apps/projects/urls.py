from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('projects.views',
    url(r'^valentines/$', 'valentines', name='valentines'),
)

