from django.shortcuts import render
from djoser.views import UserViewSet
from .serializers import FollowSerializer, FollowCreateSerializer
from .models import User, Follow
from rest_framework.decorators import action, api_view
from rest_framework import filters, permissions, serializers, status, viewsets
from rest_framework.response import Response
from api.pagination import LimitPageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from .permissions import OwnerOrReadOnly


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
    permission_classes = (permissions.IsAuthenticated, OwnerOrReadOnly)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FollowSerializer
        return FollowCreateSerializer

    def perform_create(self, serializer):
        following = get_object_or_404(User, pk=self.kwargs.get('users_id'))
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save(user=self.request.user, following=following)

    def destroy(self, request, users_id):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        instance = Follow.objects.filter(
            following=users_id, user=request.user
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

