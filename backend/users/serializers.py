from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Recipe
from rest_framework import serializers
from users.models import Follow, User


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
    """Обрабатывает эндпоинт /api/users/me/"""
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)


class RecipeShortSerializer(serializers.ModelSerializer):
    """Вспомогательный сериализатор для FollowSerializer"""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowCreateSerializer(serializers.ModelSerializer):
    """Обрабатывает запросы на добавление/удаление из подписок"""

    def to_representation(self, value):
        """Отклик на POST запрос обрабатывается другим сериализатором"""
        return FollowSerializer(
            value.following,
            context={
                'request': self.context.get('request')
            }
        ).data

    def validate(self, data):
        request = self.context.get('request')
        user = self.context.get('request').user
        my_view = self.context['view']
        object_id = my_view.kwargs.get('users_id')
        if Follow.objects.filter(
            user=user,
            following=object_id
        ).exists() and request.method == 'POST':
            raise serializers.ValidationError({
                'errors': 'Пользователь уже добавлен в подписки'})
        if not Follow.objects.filter(
            user=user,
            following=object_id
        ).exists() and request.method == 'DELETE':
            raise serializers.ValidationError({
                'errors': 'Вы не подписаны на этого пользователя'})
        if (user.id == int(object_id)
                and self.context['request'].method == 'POST'):
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        return data

    class Meta:
        model = Follow
        fields = '__all__'
        read_only_fields = (
            'user',
            'following'
        )


class FollowSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit_recipes = request.query_params.get('recipes_limit')
        if limit_recipes:
            recipes = obj.author_of_recipe.all()[:(int(limit_recipes))]
        else:
            recipes = obj.author_of_recipe.all()
        context = {'request': request}
        return RecipeShortSerializer(recipes, many=True, context=context).data

    def get_recipes_count(self, obj):
        return obj.author_of_recipe.all().count()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
