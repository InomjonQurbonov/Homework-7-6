from django.urls import path
from .views import (
    index, RegistrationView, NewsAddView,
    NewsListView, NewsDetailView, UpdateNewsView,
    DeleteNewsView
)

urlpatterns = [
    path('', index, name='home'),
    path('register/', RegistrationView.as_view(), name='registration'),
    path('add_news/', NewsAddView.as_view(), name='add_news'),
    path('news_list/', NewsListView.as_view(), name='news_list'),
    path('news_detail/<int:pk>/', NewsDetailView.as_view(), name='about_news'),
    path('update/<int:pk>/', UpdateNewsView.as_view(), name='update_news'),
    path('delete/<int:pk>/', DeleteNewsView.as_view(), name='delete_news')
]
