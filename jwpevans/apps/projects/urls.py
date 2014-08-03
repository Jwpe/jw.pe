from django.conf.urls import patterns, url

urlpatterns = patterns('projects.views',
    url(r'^valentines/$', 'valentines', name='valentines'),
)

