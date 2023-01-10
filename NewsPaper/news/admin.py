from django.contrib import admin
from .models import Author, Post, PostCategory, Category, Comment, User


admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Comment)
# admin.site.register(User)