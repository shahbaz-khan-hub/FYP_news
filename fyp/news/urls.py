from django.contrib import admin
from django.urls import path,include
from . import views



urlpatterns = [
    path('keyword/', views.extract_articles_by_keyword, name='extract_articles_by_keyword'),
    path('region/', views.extract_articles_by_region, name='extract_articles_by_region'),]
    # Add other URL patterns as needed for your project