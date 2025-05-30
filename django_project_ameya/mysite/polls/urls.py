from django.urls import path

from . import views

app_name = "polls"
from debug_toolbar.toolbar import debug_toolbar_urls
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]+debug_toolbar_urls()