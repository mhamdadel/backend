from django.urls import path
from knox import views as knox_views
from .views import RegisterAPI, LoginAPI, LogoutAPI, ProfileAPIView, MyOrder

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('myorders/', MyOrder.as_view(), name='myorders'),
]