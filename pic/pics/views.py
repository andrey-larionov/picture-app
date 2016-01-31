from pics.models import Picture
from django.contrib.auth.models import User
from pics.serializers import PictureSerializer, UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework import permissions


class CreateUserView(CreateAPIView):
    model = User
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer


class PictureList(APIView):
    """
    List all pictures, or create a new picture.
    """
    def get(self, request, format=None):
        pictures = Picture.objects.all()
        serializer = PictureSerializer(pictures, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = PictureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PictureDetail(APIView):
    """
    Get single picture
    """
    def get_object(self, pk):
        try:
            return Picture.objects.get(pk=pk)
        except Picture.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        picture = self.get_object(pk)
        serializer = PictureSerializer(picture)
        return Response(serializer.data)