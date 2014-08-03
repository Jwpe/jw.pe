from django.contrib.auth.models import User
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.text import truncate_words

from blog.managers import PublicManager


class Category(models.Model):
    """Category model."""
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        db_table = 'blog_categories'
        ordering = ('title',)

    def __unicode__(self):
        return u'{}'.format(self.title)

    def get_absolute_url(self):
        return reverse('blog:category_detail', kwargs={'slug': self.slug})


class Post(models.Model):
    """Post model."""

    STATUS_CHOICES = (
        (1, 'Draft'),
        (2, 'Public'),
    )
    # Draft ID to identify posts from draft
    draft_id = models.IntegerField(blank=True, null=True)

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique_for_date='publish')
    author = models.ForeignKey(User, blank=True, null=True)

    body = models.TextField()
    tease = models.TextField(blank=True,
        help_text='Concise text suggested. Does not appear in RSS feed.')

    status = models.IntegerField(choices=STATUS_CHOICES, default=2)
    allow_comments = models.BooleanField(default=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category, blank=True)
    objects = PublicManager()

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        db_table = 'blog_posts'
        ordering = ('-publish',)
        get_latest_by = 'publish'

    def __unicode__(self):
        return u'{}'.format(self.title)

    def get_absolute_url(self):
        return reverse('blog:blog_detail', kwargs={'slug': self.slug})

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
        return Post.objects.filter(status=2).order_by('-publish')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.tease + "..."
