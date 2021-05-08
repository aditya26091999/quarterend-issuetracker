from django.urls import path
from . import views

app_name = 'templateApp'

urlpatterns = [
    path('', views.index, name='index')
]
