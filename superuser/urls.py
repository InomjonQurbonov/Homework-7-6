from django.urls import path

from .views import send_email

urlpatterns = [
    path('superuser/', send_email, name='superuser')
]