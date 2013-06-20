# Create your views here.
from django.views.generic import ListView
from django.shortcuts import get_object_or_404

from blog.models import Category


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
