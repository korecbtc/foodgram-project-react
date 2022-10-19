from django.shortcuts import render
from djoser.views import UserViewSet
from .serializers import FollowSerializer
from .models import User, Follow
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
        users = User.objects.filter(following__user=request.user)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()

    @action(
        methods=['POST', 'DELETE'],
        detail=False,
        serializer_class=FollowSerializer,
        url_path=''
    )
    def subscribe(self, request):
        print('hello')
        Follow.objects.create(user=request.user, following=self.kwargs.get('users_id'))
        users = User.objects.filter(following__user=request.user)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)
