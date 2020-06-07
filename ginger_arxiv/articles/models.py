from django.db import models


class Article(models.Model):
    link = models.URLField(unique=True, db_index=True)
    added = models.DateField(auto_now_add=True)  # added to our system
    arxiv_published = models.DateField(blank=True, null=True)
    arxiv_updated = models.DateField(blank=True, null=True)
    title = models.CharField(max_length=255)
    summary = models.TextField()
    doi = models.CharField(max_length=25, blank=True, null=True)
    pdf_link = models.URLField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    journal = models.TextField(blank=True, null=True)

    # todo: add categories -- https://arxiv.org/help/prep#subj entry['arxiv_primary_category']['term']
    #   And allow for filtering by category, show category on lists, etc

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=255)
    articles = models.ManyToManyField(Article, related_name="Authors")
    article_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def all_articles(self):
        return self.articles.all()
