# clubs/urls.py
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('clubs/', views.clubs_all, name='clubs_all'),  # все клубы
    path('club/<int:pk>/', views.club_detail, name='club_detail'),
    path('search/', views.search, name='search'),
    path('news/', views.news_list, name='news_list'),
]

