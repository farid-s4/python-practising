from django.urls import path

from .views import *
from . import views
app_name = 'tracker'
urlpatterns = [
    path('', index, name='index'),
    path('expenses/', views.expenses_list, name='expenses'),
    path('expenses/create_expense/', views.create_expense, name='create_expense'),
    path('expenses/create_expense.html', views.create_expense),
    path('expenses/<int:expense_id>/', views.expense_detail, name='expense_detail'),
]
