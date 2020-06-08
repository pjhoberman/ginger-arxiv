import time
from datetime import date, datetime, timedelta

import feedparser

from ginger_arxiv.articles.models import Article, Author

"""
This script has a lot of print statements. It was useful for ensuring
the right articles were imported and that occasional failing calls
were resolved. I'm leaving them in here so that fresh imports have
obvious call patterns.

In addition, I decided to convert all datetimes to dates, as the time of
publication didn't seem relevant, and it was easier for a short project to
ignore timezones.
"""

# limit to: psychiatry, therapy, data science or machine learning
Q = [
    "all:psychiatry",
    "all:therapy",
    'all:"data science"',
    'all:"machine learning"',
]
Q = "+OR+".join([term.replace(" ", "+").replace('"', "%22") for term in Q])


def convert_date(d: str):
    # atom format: 2007-02-27T16:02:02-05:00
    # return format: date(2007, 02, 27)
    d = datetime.strptime(d, "%Y-%m-%dT%H:%M:%S%z") if d else None
    return date(d.year, d.month, d.day) if d else None


def call_arxiv_api(test: bool = False):
    base_url = f"http://export.arxiv.org/api/query?search_query={Q}&sortBy=submittedDate&sortOrder=descending"
    start = 0
    max_results = 1000
    url = f"{base_url}&start={start}&max_results={max_results}"

    six_months_ago = date.today() - timedelta(weeks=26)
    print(f"retrieving results {start} - {max_results}")
    print(url)
    d = feedparser.parse(url)
    while len(d.entries) > 0:
        # stop importing if the first result is older than 6 months old
        if convert_date(d.entries[0]["published"]) < six_months_ago:
            print("Reached 6 months ago")
            break
        keep_going = get_articles(d.entries)
        if test or not keep_going:
            break
        start += max_results
        print(f"retrieving results {start} - {start+max_results}")
        url = f"{base_url}&start={start}&max_results={max_results}"
        print(url)
        for i in range(10):  # sometimes the results don't come back, try a few times.
            print(f"Trying url - attempt #{i+1} - Sleeping for {i} seconds")
            time.sleep(i)  # wait longer each time
            d = feedparser.parse(url)
            print("Entries: ", len(d.entries))
            if len(d.entries):
                print("it worked! grabbing entries")
                break


def get_articles(entries):
    for entry in entries:
        # todo: do all entries have a link?
        # see if the article is already imported
        if Article.objects.filter(link=entry.get("link")).count() > 0:
            print("Reached articles already downloaded")
            return False

        # todo: are there ever more than one PDF link?
        try:
            pdf_link = [
                link["href"] for link in entry.links if link.get("title", None) == "pdf"
            ][0]
        except IndexError:
            pdf_link = None

        article = Article.objects.create(
            link=entry.get("link", None),
            arxiv_published=convert_date(entry.get("published", None)),
            arxiv_updated=convert_date(entry.get("updated", None)),
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
            author.articles.add(article)
            author.article_count = author.articles.count()
            author.save()  # todo: time consuming but saves time later
    return True
