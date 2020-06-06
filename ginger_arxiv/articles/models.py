from django.db import models


class Article(models.Model):
    link = models.URLField(unique=True, db_index=True)
    added = models.DateTimeField(auto_now_add=True)  # added to our system
    arxiv_published = models.DateTimeField(blank=True, null=True)
    arxiv_updated = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length=255)
    summary = models.TextField()
    doi = models.CharField(max_length=25, blank=True, null=True)
    pdf_link = models.URLField(blank=True, null=True)
    details = models.CharField(max_length=255, blank=True, null=True)
    journal = models.CharField(max_length=255, blank=True, null=True)

    # todo: add categories? -- https://arxiv.org/help/prep#subj entry['arxiv_primary_category']['term']

    def __str__(self):
        return self.title

    def authors(self):
        """Returns list of author objects"""
        return [aa.author for aa in ArticleAuthor.objects.filter(article=self)]


class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ArticleAuthor(models.Model):
    author = models.ForeignKey("Author", on_delete=models.CASCADE)  # todo: index
    article = models.ForeignKey("Article", on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.author, self.article)

    class Meta:
        unique_together = ("author", "article")
