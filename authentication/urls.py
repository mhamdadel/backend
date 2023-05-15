from django.urls import path
from knox import views as knox_views
from .views import RegisterAPI, LoginAPI, LogoutAPI, ProfileAPIView, MyOrders, MyOrderDetails, MyCart, MyWishListItems

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('orders/', MyOrders.as_view(), name='myorders'),
    path('orders/<int:id>/', MyOrderDetails.as_view(), name='user_order_details'),
    path('cart/', MyCart.as_view(), name='cart'),
    path('wishlist/', MyWishListItems.as_view(), name='wishlist'),
]