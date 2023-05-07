from django.contrib import admin

# Register your models here.

# Berfore Lec 91
# from .models import Post
# admin.site.register(Post)

from blog.models import Post, BlogComment

admin.site.register((Post, BlogComment))
