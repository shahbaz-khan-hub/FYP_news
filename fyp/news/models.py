from django.db import models

# Create your models here.
class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    source_url = models.URLField()

class KeywordUrlPair(models.Model):
    keyword = models.CharField(max_length=50)
    url = models.URLField()