from rest_framework import  serializers
from rest_framework.permissions import IsAuthenticated
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password # Register serializer
from .models import Books

class RegisterSerializer(serializers.ModelSerializer):
    role_type = serializers.CharField()

    def create(self, validated_data):
        print(direction=validated_data['role_type'])

    class Meta:
        model = User
        fields = ('id','username','password','first_name', 'last_name',"role_type")
        extra_kwargs = {
            'password':{'write_only': True},
        }
        def create(self, validated_data):
            user = User.objects.create_user(validated_data['username'],
                                            password = validated_data['password'],
                                            first_name=validated_data['first_name'],
                                            last_name=validated_data['last_name'],
                                            is_superuser=1)
            return user# User serializer



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



class AddBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields=('ISBN_Code','Book_Title','Book_Author', 'Publication_year','Status','Borrowed_By')


class ISBNBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields=('ISBN_Code',)

class UpdateBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields=('ISBN_Code','Book_Title','Book_Author', 'Publication_year','Status','Borrowed_By')

class DeleteMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=('username',)


class ViewMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)