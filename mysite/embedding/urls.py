from django.urls import path

from . import views

urlpatterns = [
    # ex: /embedding/
    path('', views.home, name='index'),
    path('translation/', views.translation, name='translation'),
    path('embedding/', views.embedding, name='embedding'),
    path('answer/', views.answer, name='answer'),
]