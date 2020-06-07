from datetime import datetime, timedelta

import feedparser
import pytz

from ginger_arxiv.articles.models import Article, Author

# todo: should this be a class
# limit to: psychiatry, therapy, data science or machine learning
Q = [
    "all:psychiatry",
    "all:therapy",
    'all:"data science"',
    'all:"machine learning"',
]
Q = "+OR+".join([term.replace(" ", "+").replace('"', "%22") for term in Q])


def convert_date(date: str):
    # atom format: 2007-02-27T16:02:02-05:00
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z") if date else None


def call_arxiv_api(test: bool = False):
    base_url = f"http://export.arxiv.org/api/query?search_query={Q}&sortBy=submittedDate&sortOrder=descending"
    start = 0
    max_results = 100
    url = f"{base_url}&start={start}&max_results={max_results}"

    six_months_ago = datetime.now(pytz.utc) - timedelta(weeks=26)

    d = feedparser.parse(url)
    while len(d.entries) > 0:
        # stop importing if the first result is older than 6 months old
        if convert_date(d.entries[0]["published"]) < six_months_ago:
            break
        get_articles(d.entries)
        if test:
            break
        start = max_results
        max_results += 100
        print(f"retrieving results {start} - {max_results}")
        url = f"{base_url}&start={start}&max_results={max_results}"
        d = feedparser.parse(url)


def get_articles(entries):
    for entry in entries:
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

        title = entry.get("title", None)
        title = (
            title[:255] if title else None
        )  # save title as charfield but make sure it doesn't break

        article = Article.objects.create(
            link=entry.get("link", None),
            arxiv_published=convert_date(entry.get("published", None)),
            arxiv_updated=convert_date(entry.get("updated", None)),
            title=title,
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
            author.articles.add(article)
            author.article_count = author.articles.count()
            author.save()  # todo: time consuming but saves time later?
