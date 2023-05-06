from django.urls import path,include
from . import views

urlpatterns=[
  path('cart/',views.add_to_cart,name='add_to_cart'),
  path('',views.cart,name='cart'),
  path('cart/<int:product_id>/', views.cart_item, name='cart_item'),
]