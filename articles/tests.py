from django.test import TestCase

from .import_articles import get_articles


class TestArticleRetrieval(TestCase):
    def test_get_articles(self):
        url = "http://export.arxiv.org/api/query?search_query=all:electron&start=0&max_results=3"
        get_articles(url)
