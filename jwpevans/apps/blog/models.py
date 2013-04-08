from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import truncate_words
from django.utils.translation import ugettext_lazy as _


from blog.managers import PublicManager

import datetime

from tinymce import models as tinymce_models

class Category(models.Model):
    """Category model."""
    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        db_table = 'blog_categories'
        ordering = ('title',)

    def __unicode__(self):
        return u'%s' % self.title


    @models.permalink
    def get_absolute_url(self):
        return ('blog_category', None, {'slug': self.slug})


class Post(models.Model):
    """Post model."""
    STATUS_CHOICES = (
        (1, _('Draft')),
        (2, _('Public')),
    )
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), unique_for_date='publish')
    author = models.ForeignKey(User, blank=True, null=True)

    body = tinymce_models.HTMLField(_('body'),)
    tease = models.TextField(_('tease'), blank=True,
        help_text=_('Concise text suggested. Does not appear in RSS feed.'))

    visits = models.IntegerField(_('visits'), default=0, editable=False)
    status = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=2)
    allow_comments = models.BooleanField(_('allow comments'), default=True)
    publish = models.DateTimeField(_('publish'), default=timezone.now)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    categories = models.ManyToManyField(Category, blank=True)
    objects = PublicManager()

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        db_table = 'blog_posts'
        ordering = ('-publish',)
        get_latest_by = 'publish'

    def __unicode__(self):
        return u'%s' % self.title

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug':self.slug})

    def get_disqus_url(self):
        """
        Necessary because django-disqus doesn't seem to automatically
        add the site to absolute urls. This could be because it's in
        development mode, however.
        """
        return ''.join(settings.SITE_DOMAIN, '/blog/post/', self.slug)

    def get_previous_post(self):
        return self.get_previous_by_publish(status__gte=2)

    def get_next_post(self):
        return self.get_next_by_publish(status__gte=2)

    @property
    def get_meta_description(self):
        return truncate_words(self.tease, 255) or None


class LatestEntriesFeed(Feed):
    title = "Jonathan Evans' Blog"
    link = "/blog/"
    description = "Insert description here."

    def items(self):
        return Post.objects.filter(
        status = 2,
        ).order_by('-publish')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        description = (item.tease + "...")
        return description