from pics.models import Picture, PictureRate
from django.contrib.auth.models import User
from pics.serializers import PictureSerializer, PictureRateSerializer, UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework import permissions


class UserList(CreateAPIView):
    model = User
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


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


class PictureList(APIView):
    """
    List all pictures, or create a new picture.
    """
    def get(self, request, format=None):
        uid = request.query_params.get('u', None)
        # If 'u' parameter don't exists in query
        # then return all pictures
        if uid == None:
            pictures = Picture.objects.all()
        else:
            # Else try to find pictures by user id
            # taken from 'u' parameter
            try:
                user = User.objects.get(pk=int(uid))
                pictures = Picture.objects.filter(user=user)
            # If user was not found by id return empty set
            except:
                pictures = []
           
        
        serializer = PictureSerializer(pictures, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = PictureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PictureRateDetail(APIView):

    def get_object(self, pk):
        try:
            return PictureRate.objects.get(pk=pk)
        except PictureRate.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        picture_rate = self.get_object(pk)
        serializer = PictureRateSerializer(
            picture_rate, 
            context={'request': request}
        )
        return Response(serializer.data)


class PictureRateList(APIView):

    def get(self, request, format=None):
        picture_rates = PictureRate.objects.all()
        serializer = PictureRateSerializer(
            picture_rates, many=True, 
            context={'request': request}
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = PictureRateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
class PictureRated(APIView):

    def get(self, request, format=None):
        picture_rates = PictureRate.objects.filter(user=request.user)
        # Get pictures from user's rates
        pictures = [rate.picture for rate in picture_rates]
        serializer = PictureSerializer(
            pictures, 
            many=True, 
            context={'request': request}
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)