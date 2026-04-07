from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


app_name = 'finance'

urlpatterns = [
   
    path('', views.index, name='index'),
    path('transactions/', views.transactions, name='transactions'),
    path('transactions/new/', views.add_transaction, name='add_transaction'),
    path('api/transactions/', views.transactions_api, name='transactions_api'),
    path('api/transactions/add/', views.add_transaction_api, name='add_transaction_api'),
    path('api/summary/', views.finance_summary_api, name='finance_summary_api'),
]