from django.urls import path

from ginger_arxiv.articles import views

app_name = "articles"
urlpatterns = [
    path("", views.list_articles, name="list_articles"),
    path("author/<int:author_pk>", views.author_detail, name="author_detail"),
]
