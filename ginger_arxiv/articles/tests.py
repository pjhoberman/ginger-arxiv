from django.test import TestCase

from .import_articles import get_articles
from .models import Article


class TestArticleRetrieval(TestCase):
    def test_get_articles(self):
        # No articles initially
        self.assertEqual(Article.objects.count(), 0)

        # This url should return 3 results -- fragile test as it relies on 3rd party
        url = "http://export.arxiv.org/api/query?search_query=all:electron&start=0&max_results=3"
        get_articles(url)
        self.assertEqual(Article.objects.count(), 3)

        # Code should not re-add articles
        get_articles(url)
        self.assertEqual(Article.objects.count(), 3)
