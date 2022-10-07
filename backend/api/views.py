from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from users.models import User
from rest_framework import filters, permissions, serializers, status, viewsets
from djoser.views import UserViewSet

# @api_view(['POST'])
# def signup(request):
#     serializer = CustomUserSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         user = get_object_or_404(
#             User, username=serializer.validated_data.get('username')
#         )
#         user.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

