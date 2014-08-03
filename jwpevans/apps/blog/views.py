from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

import json

from blog.models import Post, Category


class CategoryListView(ListView):

    context_object_name = "posts"
    template_name = "blog/category_detail.html"

    def get_queryset(self):

        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return self.category.post_set.all()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CategoryListView, self).get_context_data(**kwargs)
        # Add in the category
        context['category'] = self.category
        return context


def process_draft_post(request):

    if request.method == 'POST':
        data = json.loads(request.raw_post_data)
        if data:
            try:
                draft_id = data['id']
                title = data['name']
                body = data['content']
            except KeyError:
                return
            try:
                post = Post.objects.get(draft_id=draft_id)
            except Post.DoesNotExist:
                post = Post(draft_id=draft_id)

            author = User.objects.get(username='Jonathan')

            post.title = title
            post.slug = slugify(title.decode())
            post.body = body
            post.tease = body[:200] + '...'
            post.author = author

            post.save()

            response = HttpResponse()
            response['location'] = post.get_absolute_url()

            return response

    raise Http404
