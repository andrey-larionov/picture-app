from rest_framework import serializers, viewsets
from rest_framework.response import Response
from pics.models import Picture
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.HyperlinkedModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

class PictureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Picture
        fields = ('id', 'created', 'image', 'average_rate')
        user = serializers.Field(source='user.username')