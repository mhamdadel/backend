from django.urls import path,include
from . import views

urlpatterns=[
    path('list/', views.order_list, name='order_list'),
    path('add_order/', views.add_order, name='add_order'),
    # path('add_order_item/', views.add_order_item, name='add_order_item'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
]