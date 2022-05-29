from django.contrib import admin
from .models import Author, Category, Comment, Post, PostCategory

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'datetime', 'author', 'rating', 'text')
    list_filter = ('datetime', 'rating', 'author')

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('authorUser', 'ratingAuthor')
    list_filter = ('authorUser', 'ratingAuthor')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('commentUser', 'text', 'dateCreation', 'rating')
    list_filter = ('commentUser', 'text', 'dateCreation', 'rating')

admin.site.register(Author, AuthorAdmin)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment, CommentAdmin)