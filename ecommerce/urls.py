from django.urls import path
from .views import CategoryDetail, CategoryList, UploadImage


urlpatterns = [
    path('categories/', CategoryList.as_view()),
    path('categories/<str:name>/', CategoryDetail.as_view()),
    path("image/upload", UploadImage.as_view())
]


