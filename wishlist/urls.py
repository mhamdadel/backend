from django.urls import path,include
from . import views

urlpatterns=[
  path('',views.wishlist_crud,name='wishlist_crud'),
  path('<int:id>', views.wishlist_delete, name='wishlist_delete'),
]
