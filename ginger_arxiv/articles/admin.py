from django.contrib import admin

from .models import Article, ArticleAuthor, Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]
    # todo: show articles


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        "arxiv_published",
        "title",
        "link",
    ]
    # todo: show authors


@admin.register(ArticleAuthor)
class ArticleAuthorAdmin(admin.ModelAdmin):
    list_display = ["article", "author"]
