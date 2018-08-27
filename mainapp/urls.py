from django.urls import path

from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.index, name='index'),
    path('details/<int:pk>', views.details, name='details'),
    path('products/', views.products, name='products'),
    path('products/<int:category_pk>', views.products, name='products_by_category'),
    path('contacts', views.contacts, name='contacts'),
]
