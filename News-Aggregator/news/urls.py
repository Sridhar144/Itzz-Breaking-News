from django.urls import path
from news.views import scrape, news_list, predictor
urlpatterns = [
  path('scrape/<str:name>', scrape, name="scrape"),
  path('predictor', predictor, name="predictor"),
  # path('success_url', name="success"),
  path('', news_list, name="home"),
]