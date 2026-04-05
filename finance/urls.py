from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


app_name = 'finance'

urlpatterns = [
   
    path('', views.index, name='index'),
    path('transactions/', views.transactions, name='transactions'),
    path('transactions/new/', views.add_transaction, name='add_transaction'),
    path('api/transactions/', views.transactions_api, name='transactions_api'),
    
]