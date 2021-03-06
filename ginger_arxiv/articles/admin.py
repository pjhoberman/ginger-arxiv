from django.contrib import admin

from .models import Article, Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        "arxiv_published",
        "title",
        "link",
    ]
