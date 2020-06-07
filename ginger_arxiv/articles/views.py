from django.shortcuts import get_object_or_404, render

from .models import Article, Author


def list_articles(request):
    articles = Article.objects.all()  # todo: check requirements
    return render(request, "articles/list.html", {"articles": articles})


def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    return render(request, "articles/article_detail.html", {"article": article})


def author_list(request):
    authors = Author.objects.all().order_by("name")
    return render(request, "articles/author_list.html", {"authors": authors})


def author_detail(request, author_pk):
    author = get_object_or_404(Author, pk=author_pk)
    return render(request, "articles/author_detail.html", {"author": author})
