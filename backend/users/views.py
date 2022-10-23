from django.shortcuts import get_object_or_404

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from djoser.views import UserViewSet

from .models import Follow, User
from .pagination import LimitPageNumberPagination
from .permissions import OwnerOrReadOnly
from .serializers import FollowCreateSerializer, FollowSerializer


class CustomUserViewSet(UserViewSet):
    pagination_class = LimitPageNumberPagination
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny, ]

    @action(
        methods=['GET'],
        detail=False,
        serializer_class=FollowSerializer,
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscriptions(self, request):
        users = User.objects.filter(following__user=request.user)
        pages = self.paginate_queryset(users)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class FollowViewSet(viewsets.ModelViewSet):
    """Эндпоинт api/users/subscriptions/"""
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()
    permission_classes = (permissions.IsAuthenticated, OwnerOrReadOnly)
    pagination_class = LimitPageNumberPagination

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

        return serializer.save(user=self.request.user, following=following)

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
