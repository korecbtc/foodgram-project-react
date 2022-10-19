from django.shortcuts import render
from djoser.views import UserViewSet
from .serializers import FollowSerializer
from .models import User
from rest_framework.decorators import action, api_view
from rest_framework import filters, permissions, serializers, status, viewsets
from rest_framework.response import Response
from api.pagination import LimitPageNumberPagination


class CustomUserViewSet(UserViewSet):
    pagination_class = LimitPageNumberPagination
    queryset = User.objects.all()

    @action(
        methods=['GET'],
        detail=False,
        serializer_class=FollowSerializer
    )
    def subscriptions(self, request):
        print('hello')
        users = User.objects.filter(following__user=request.user)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)
