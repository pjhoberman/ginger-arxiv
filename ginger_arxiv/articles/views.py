from django.shortcuts import get_object_or_404, render

from .models import Article, Author


def list_articles(request):
    articles = Article.objects.all()  # todo: check requirements
    return render(request, "articles/list.html", {"articles": articles})


def author_detail(request, author_pk):
    author = get_object_or_404(Author, pk=author_pk)
    return render(request, "articles/author_detail.html", {"author": author})
