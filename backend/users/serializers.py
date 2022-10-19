from typing_extensions import Required
from django.forms import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import User, Follow
from recipes.models import Recipe
from djoser.serializers import UserSerializer, UserCreateSerializer, TokenCreateSerializer


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        """Метод определяет подписан ли текущий пользователь на автора"""
        request = self.context.get('request')
        if request.user.is_anonymous or request is None:
            return False
        return Follow.objects.filter(user=request.user, following=obj).exists()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)


class RecipeShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()

    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(author=obj)
        request = self.context.get('request')
        return RecipeShortSerializer(
            recipes, many=True,
            context={'request': request}
        ).data

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes'
            # 'recipes_count'
        )
