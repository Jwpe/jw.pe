from django.conf import settings
from django.conf.urls.defaults import patterns, url
from django.views.generic import (ListView, DetailView, DayArchiveView,
    MonthArchiveView, YearArchiveView)

from blog.views import CategoryListView, process_draft_post
from blog.models import Post, LatestEntriesFeed

urlpatterns = patterns('',

    #Returns all blog posts (paginated)
    url(r'^$',
        ListView.as_view(model=Post, paginate_by=5,
            context_object_name="posts"), name="blog_index"),
    #Returns one blog post (based on slug)
    url(r'^post/(?P<slug>[-\w]+)/$',
        DetailView.as_view(model=Post, context_object_name="post"),
        name="blog_detail"),
    #Returns the blog posts for a certain day
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{1,2})/$',
        DayArchiveView.as_view(model=Post, paginate_by=5,
            context_object_name="posts", month_format='%m',
            date_field='publish'), name="blog_archive_day"),
    #Returns the blog posts for a certain month
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        MonthArchiveView.as_view(model=Post, paginate_by=5,
            context_object_name="posts", month_format='%m',
            date_field='publish', allow_empty=True),
        name="blog_archive_month"),
    #Returns the blog posts for a certain year
    url(r'^(?P<year>\d{4})/$',
        YearArchiveView.as_view(model=Post, date_field='publish',
            allow_empty=True), name="blog_archive_year"),
    #Returns the blog posts for a certain category
    url(r'^categories/(?P<slug>[-\w]+)/$',
        CategoryListView.as_view(allow_empty=True, paginate_by=5),
        name="category_detail"),
    #RSS URL
    url(r'rss/$', LatestEntriesFeed()),
    # Draft post URL
    url(r'^{}/'.format(settings.DRAFT_POST_URL), process_draft_post,
        name='process_draft_post'),
)
