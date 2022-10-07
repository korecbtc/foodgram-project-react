from django.shortcuts import render
from djoser.views import UserViewSet
from .serializers import CustomUserSerializer
from .models import User
from rest_framework.decorators import action, api_view
from rest_framework import filters, permissions, serializers, status, viewsets
from rest_framework.response import Response

class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


