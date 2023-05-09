from django.urls import path
from .views import CategoryDetail, CategoryList, UploadImage, ProductList, ProductDetail


urlpatterns = [
    path('categories/', CategoryList.as_view()),
    path('categories/<str:name>/', CategoryDetail.as_view()),
    path("image/upload", UploadImage.as_view()),
    path('products/', ProductList.as_view()), 
    path('products/<str:title>/',ProductDetail.as_view())
]


