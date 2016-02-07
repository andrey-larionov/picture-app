from rest_framework import serializers, viewsets
from rest_framework.response import Response
from pics.models import Picture, PictureRate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

class UserSerializer(serializers.HyperlinkedModelSerializer):
    email = serializers.EmailField(
        required=True, 
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        read_only_fields = ('id',)
        extra_kwargs = {'password': {'write_only': True}}

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


class PictureRateSerializer(serializers.HyperlinkedModelSerializer):
    picture = serializers.PrimaryKeyRelatedField(queryset=Picture.objects.all())

    class Meta:
        model = PictureRate
        fields = ('url', 'id', 'rate', 'picture')
        user = serializers.Field(source='user.username')

    def unique_user_picture_validate(self, user, picture):
        picture_rate = PictureRate.objects.filter(user=user, picture=picture)
        if picture_rate:
            raise serializers.ValidationError("You are already voted this picture.")

    def range_validator(self, value):
        if value not in range(1, 11):
            raise serializers.ValidationError("Rate value should be in range 1 .. 10.")

    def create(self, validated_data):
        picture = validated_data['picture']
        user = validated_data['user']
        rate = validated_data['rate']
        
        self.range_validator(value=validated_data['rate'])
        self.unique_user_picture_validate(
            user=user, 
            picture=picture
        )

        picture_rate = PictureRate.objects.create(
            picture=picture,
            user=user,
            rate=rate
        )
        picture_rate.save()
        picture.calc_average_rate()
        picture.save()

        return picture_rate