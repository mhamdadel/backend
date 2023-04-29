from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view 
from .models import Base
from .serializers import BaseSerializer

@api_view(['GET', 'POST'])
def all_base(request):
    if request.method == 'GET':
        bases = Base.objects.all()
        serializer =  BaseSerializer(bases, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        serializer = BaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET', 'PATCH', 'DELETE'])
def base_detail(request, id):
    try :
        myBase = Base.objects.get(pk=id)
    except Base.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BaseSerializer(myBase)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'PATCH':
        serializer = BaseSerializer(myBase, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        myBase.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)