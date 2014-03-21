from django.contrib import admin
from blog.models import Post, Category



class PostAdmin(admin.ModelAdmin):
    list_display  = ('title', 'publish', 'status',)
    list_filter   = ('publish', 'categories', 'status')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
