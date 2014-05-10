from django.contrib.sitemaps import Sitemap
from .models import Post, Category

class PostSitemap(Sitemap):
    changefreq = "never"
    priority = 0.7

    def items(self):
        return Post.objects.filter(status=2)

    def lastmod(self, obj):
        return obj.modified

class CategorySitemap(Sitemap):
    changefreq = "never"
    priority = 0.3

    def items(self):
        return Category.objects.all()

