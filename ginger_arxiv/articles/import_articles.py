import feedparser

from .models import Article, ArticleAuthor, Author

# todo: should this be a class


def get_articles(url: str):
    d = feedparser.parse(url)
    for entry in d.entries:
        # todo: do all entries have a link?
        # see if the article is already imported
        if Article.objects.filter(link=entry.get("link")).count() > 0:
            continue

        # todo: are there ever more than one PDF link?
        try:
            pdf_link = [
                link["href"] for link in entry.links if link.get("title", None) == "pdf"
            ][0]
        except IndexError:
            pdf_link = None

        article = Article.objects.create(
            link=entry.get("link", None),
            arxiv_published=entry.get("published", None),
            arxiv_updated=entry.get("updated", None),
            title=entry.get("title", None),
            summary=entry.get("summary", None),
            doi=entry.get("arxiv_doi, None"),
            pdf_link=pdf_link,
            details=entry.get("arxiv_comment", None),
            journal=entry.get("arxiv_journal_ref", None),
        )

        for author_name in [author.name for author in entry["authors"]]:
            author, created = Author.objects.get_or_create(
                name=author_name, defaults={"name": author_name}
            )
            ArticleAuthor.objects.create(article=article, author=author)
