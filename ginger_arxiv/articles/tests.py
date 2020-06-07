import feedparser
from django.test import TestCase

from ginger_arxiv.articles.import_articles import call_arxiv_api, get_articles
from ginger_arxiv.articles.models import Article


class TestArticleRetrieval(TestCase):
    def test_get_articles(self):
        # No articles initially
        self.assertEqual(Article.objects.count(), 0)

        # This url should return 3 results -- fragile test as it relies on 3rd party
        url = "http://export.arxiv.org/api/query?search_query=all:electron&start=0&max_results=3"
        d = feedparser.parse(url)
        get_articles(d.entries)
        self.assertEqual(Article.objects.count(), 3)

        # Code should not re-add articles
        get_articles(d.entries)
        self.assertEqual(Article.objects.count(), 3)

    def test_pagination(self):
        self.assertEqual(Article.objects.count(), 0)
        call_arxiv_api(test=True)

        self.assertEqual(Article.objects.count(), 100)

        # Further tests to run:
        # - Does call stop when it reaches 6+ months
