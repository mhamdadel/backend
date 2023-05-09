from django.urls import path,include
from . import views

urlpatterns=[
  path('add',views.add_to_cart,name='add_to_cart'),
  path('',views.cart,name='cart'),
  path('<int:product_id>', views.cart_item, name='cart_item'),
]
