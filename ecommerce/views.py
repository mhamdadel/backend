from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import CategorySerializer,ProductSerilaizer
from .models import Category, Product
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_staff
    
class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'name'

    def get(self, request, name):
        try:
            queryset = self.get_queryset().filter(name=name)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data[0])
        except Exception as e:
            return Response({
                "message": str(e),
            })
    
    def patch(self, request, name):
        queryset = self.get_queryset().filter(name=name)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    
    def delete(self, request, name):
        queryset = self.get_queryset().filter(name=name)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerilaizer


    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        return Response(serializer.data)
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerilaizer
    lookup_field = 'title'

    def get(self, request, title):
        try:
            queryset = Product.objects.get(title = title)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data[0])
        except Exception as e:
            return Response({
                "message": str(e),
            })
    
    def patch(self, request, title):
        queryset = self.get_queryset().filter(title=title)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    
    def delete(self, request, title):
        queryset = self.get_queryset().filter(title=title)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class APiProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerilaizer
    pagination_class = PageNumberPagination

    def get(self, request):
        queryset = self.queryset
        category = request.GET.get('category', None)
        product = request.GET.get('product', None)
        sort = request.GET.get('sort', None)  # asc 1 && desc 0
        
        if category:
            queryset = queryset.filter(Category__name__icontains=category)

        if product:
            queryset = queryset.filter(title__icontains=product)
        
        if sort:
            if sort == '1':
                queryset = queryset.order_by('price')
            elif sort == '0':
                queryset = queryset.order_by('-price')

        paginated_queryset = self.paginate_queryset(queryset)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)





class UploadImage(CreateAPIView):

    serializer_class = ProductSerilaizer
    parser_classes = (MultiPartParser,)
    queryset = Product.objects.all()