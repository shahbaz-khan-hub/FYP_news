from django.shortcuts import render
from newspaper import Article
from textblob import TextBlob

import requests
from .models import NewsArticle, KeywordUrlPair
from django.http import JsonResponse
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from .models import NewsArticle, KeywordUrlPair
from django.contrib import admin
import nltk
from django.http import HttpResponse

nltk.download('stopwords')

NEWSAPI_API_KEY = "b1aec816d10b4665830fab8552c2391d"

def extract_articles_by_keyword(request):
    articles = []
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        print(keyword)
        # Use the keyword to fetch articles from News API
        url = f"https://newsapi.org/v2/everything?q={keyword}&apiKey={NEWSAPI_API_KEY}"
        response = requests.get(url)
        data = response.json()
        articles = data.get("articles", [])
        for article_data in articles:
            NewsArticle.objects.create(
                title=article_data.get("title", "Title not available"),
                content=article_data.get("content", "Content not available"),
                source_url=article_data.get("url", "Source URL not available")
            )
        extract_keywords_and_store()

        
        articles = NewsArticle.objects.all()[:10]
        urls_selected_articles = [article.source_url for article in articles]
        analyzed_articles = []
        for article in urls_selected_articles:
            analyzed_article = summarize_and_analyze(article)
            analyzed_articles.append(analyzed_article)
        
    return render(request, 'index.html', {'articles': analyzed_articles})

def extract_articles_by_region(request):
    articles= []
    if request.method == 'GET':
        region = request.GET.get('region')
        # Fetch articles based on the region from News API
        url = f"https://newsapi.org/v2/everything?q={region}&apiKey={NEWSAPI_API_KEY}"
        response = requests.get(url)
        data = response.json()
        articles = data.get("articles", [])

        for article_data in articles:
                NewsArticle.objects.create(
                title=article_data.get("title", "Title not available"),
                content=article_data.get("content", "Content not available"),
                source_url=article_data.get("url", "Source URL not available")
                 )
        extract_keywords_and_store()

           
        articles = NewsArticle.objects.all()[:10]
        urls_selected_articles = [article.source_url for article in articles]
        analyzed_articles = []
        for article in urls_selected_articles:
            analyzed_article = summarize_and_analyze(article)
            analyzed_articles.append(analyzed_article)
            print(analyzed_articles)
        
    return render(request, 'index.html', {'articles': analyzed_articles})
   
       

def summarize_and_analyze(url):
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()

    article_summary = article.summary

    analysis = TextBlob(article.text)
    sentiment_score = analysis.sentiment.polarity

    # Determine sentiment
    if sentiment_score > 0:
        sentiment = "Positive"
    elif sentiment_score < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return article_summary, sentiment, sentiment_score



def extract_keywords_and_store():
    articles = NewsArticle.objects.all()
    stop_words = set(stopwords.words('english'))

    for article in articles:
        body = article.content
        url = article.source_url

        words = word_tokenize(body.lower())
        # remove stopwords and then remove dublpicate keywords
        filtered_words = set(word for word in words if word.isalnum() and word not in stop_words)

        # Save 
        for word in filtered_words:
            # Check 
            keyword_entry, created = KeywordUrlPair.objects.get_or_create(keyword=word)
            # Add  URL to  KeywordUrlPair
            keyword_entry.url.add(url)

    return JsonResponse({'message': 'Keywords extracted and stored successfully.'})
