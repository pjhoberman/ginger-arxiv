# from datetime import date, timedelta

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .import_articles import call_arxiv_api
from .models import Article, Author


def list_articles(request):
    articles = Article.objects.all().order_by("-arxiv_published", "-added")
    paginator = Paginator(articles, 20)
    page_number = request.GET.get("page")
    page_articles = paginator.get_page(page_number)
    return render(request, "articles/list.html", {"articles": page_articles})


def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    return render(request, "articles/article_detail.html", {"article": article})


def author_list(request):
    authors = Author.objects.all().order_by("-article_count")
    paginator = Paginator(authors, 20)
    page_number = request.GET.get("page")
    page_authors = paginator.get_page(page_number)
    return render(request, "articles/author_list.html", {"authors": page_authors})


def author_detail(request, author_pk):
    author = get_object_or_404(Author, pk=author_pk)
    return render(request, "articles/author_detail.html", {"author": author})


def import_articles(request):
    # article_count = None
    message = None
    if request.GET.get("test", None):
        call_arxiv_api.delay(test=True)
        message = "test"

    elif request.GET.get("call", None):
        call_arxiv_api.delay(test=True)  # todo: remove test
        # article_count = Article.objects.filter(
        #     added__gt=date.today() - timedelta(days=1)
        # ).count()
        message = "real"
        # todo: send some sort of message when collection is done

    return render(request, "articles/import_articles.html", {"message": message})
