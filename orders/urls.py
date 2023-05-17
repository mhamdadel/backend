from django.urls import path,include
from . import views

urlpatterns=[
    path('list/', views.order_list, name='order_list'),
    path('add_order/', views.add_order, name='add_order'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    path('orders/<int:order_id>/delete/', views.delete_order, name='delete_order'),

]