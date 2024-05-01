from django.urls import path
from . import views


urlpatterns = [
    path('/concerts', views.prediction_concert, name='prediction_concert'),
    path('/sports', views.prediction_sports, name='prediction_sports')
]