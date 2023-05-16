from django.urls import path,include
from . import views

urlpatterns=[
  path('',views.wishlist_view,name='wishlist_view'),
  path('add/', views.wishlist_add, name='wishlist_add'),
  path('<int:id>', views.wishlist_delete, name='wishlist_delete'),
]
