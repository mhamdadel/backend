from django.urls import path
from .views import CategoryDetail, CategoryList, UploadImage, ProductList, ProductDetail, APiProductListView


urlpatterns = [
    path('categories/', CategoryList.as_view()),
    path('categories/<str:name>/', CategoryDetail.as_view()),
    path("image/upload", UploadImage.as_view()),
    path('products/', ProductList.as_view()), 
    path('productslist/', APiProductListView.as_view()), 

    path('products/<int:id>/',ProductDetail.as_view())
]
 

