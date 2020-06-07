from django.urls import path

from ginger_arxiv.articles import views

app_name = "articles"
urlpatterns = [
    path("", views.list_articles, name="list_articles"),
    path("article/<int:article_pk>", views.article_detail, name="detail"),
    path("authors", views.author_list, name="author_list"),
    path("authors/<int:author_pk>", views.author_detail, name="author_detail"),
    path("import_articles", views.import_articles, name="import_articles"),
]
