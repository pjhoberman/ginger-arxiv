from django.shortcuts import render

from .models import Article


def list_articles(request):
    articles = Article.objects.all()  # todo: check requirements
    return render(request, "articles/list.html", {"articles": articles})
