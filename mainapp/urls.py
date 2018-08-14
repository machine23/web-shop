from django.urls import path
from . import views


app_name = 'shop'
urlpatterns = [
    path('', views.index, name='index'),
    path('details/', views.details, name='details'),
    path('products/', views.products, name='products'),
    path('contacts', views.contacts, name='contacts'),
]