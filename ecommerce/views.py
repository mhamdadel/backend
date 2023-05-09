from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import CategorySerializer,ProductSerilaizer
from .models import Category, Product
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser


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
    


class ProductList(generics.ListCreateAPIView):
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
    

class UploadImage(CreateAPIView):

    serializer_class = ProductSerilaizer
    parser_classes = (MultiPartParser,)
    queryset = Product.objects.all()