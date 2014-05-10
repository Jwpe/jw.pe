from django.contrib import sitemaps
from django.core.urlresolvers import reverse

from blog.sitemap import PostSitemap, CategorySitemap

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['landing:landing', 'landing:about']

    def location(self, item):
        return reverse(item)

sitemaps = {
    'posts': PostSitemap,
    'categories': CategorySitemap,
    'static':StaticViewSitemap,
}