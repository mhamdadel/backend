from django.urls import path,include
from . import views

urlpatterns=[
  path('wishlist/',views.wishlist_crud,name='wishlist_crud'),
  path('wishlist/<int:id>/', views.wishlist_delete, name='wishlist_delete'),
]