# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'ordering': ('title',),
                'db_table': 'blog_categories',
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('draft_id', models.IntegerField(null=True, blank=True)),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique_for_date=b'publish')),
                ('body', models.TextField()),
                ('tease', models.TextField(help_text=b'Concise text suggested. Does not appear in RSS feed.', blank=True)),
                ('status', models.IntegerField(default=2, choices=[(1, b'Draft'), (2, b'Public')])),
                ('allow_comments', models.BooleanField(default=True)),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('categories', models.ManyToManyField(to='blog.Category', blank=True)),
            ],
            options={
                'ordering': ('-publish',),
                'db_table': 'blog_posts',
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
                'get_latest_by': 'publish',
            },
        ),
    ]
