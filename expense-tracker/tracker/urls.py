from django.urls import path

from .views import *
from . import views
app_name = 'tracker'
urlpatterns = [
    path('', index),
    path('expenses/', views.expenses_list, name='expenses'),
]