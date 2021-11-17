from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import UserSerializer, LoginSerializer
from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth import authenticate


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=request.data['username'], password=request.data['password'])
        
        if user is not None:
            token = Token.objects.get_or_create(user=user)[0]

            return Response({'token': token.key})
            
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class AccountView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
    
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        find_user = User.objects.filter(username=request.data['username']).exists()
        
        if find_user == True:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(**serializer.validated_data)

        serializer = UserSerializer(user)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)