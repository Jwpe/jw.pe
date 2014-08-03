from django.conf.urls import patterns, url
from django.views.generic import TemplateView


urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="landing/landing.html"),
        name="landing"),
    url(r'^about/$', TemplateView.as_view(
        template_name='landing/about.html'), name='about'),
)
