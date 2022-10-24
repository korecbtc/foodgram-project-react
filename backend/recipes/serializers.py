import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from users.serializers import CustomUserSerializer

from .models import (
    Favorite,
    Ingredient,
    IngredientRecipe,
    Recipe,
    ShoppingCart,
    Tag
)


class Base64ImageField(serializers.ImageField):
    """Кастомное поле для картинки"""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Обрабатывает эндпоинт /api/recipes/{id}/shopping_cart/"""
    main_model = ShoppingCart
    id = serializers.ReadOnlyField(
        source='recipe.id',
    )
    name = serializers.ReadOnlyField(
        source='recipe.name',
    )
    image = serializers.CharField(
        source='recipe.image',
        read_only=True,
    )
    cooking_time = serializers.ReadOnlyField(
        source='recipe.cooking_time',
    )

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'image', 'cooking_time')

    def validate(self, data):
        request = self.context.get('request')
        user = self.context.get('request').user
        my_view = self.context['view']
        object_id = my_view.kwargs.get('recipes_id')
        if not Recipe.objects.filter(id=object_id).exists():
            raise serializers.ValidationError({
                'errors': 'Рецепт не найден'})
        if self.main_model.objects.filter(
            user=user,
            recipe=object_id
        ).exists() and request.method == 'POST':
            raise serializers.ValidationError({
                'errors': 'Рецепт уже добавлен в список'})
        if not self.main_model.objects.filter(
            user=user,
            recipe=object_id
        ).exists() and request.method == 'DELETE':
            raise serializers.ValidationError({
                'errors': 'Рецепт не находится в списке'})
        return data


class FavoriteSerializer(ShoppingCartSerializer):
    """Обрабатывает эндпоинт /api/recipes/{id}/favorite/"""
    main_model = Favorite

    class Meta(ShoppingCartSerializer.Meta):
        model = Favorite


class IngredientSerializer(serializers.ModelSerializer):
    """Обрабатывает эндпоинт /api/ingredients/"""
    class Meta:
        model = Ingredient
        fields = (
            'id', 'name', 'measurement_unit'
        )


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Обрабатывает данные из 2ух моделей. Таким образом,
    к ингредиентам добавляется поле "amount"."""
    id = serializers.ReadOnlyField(source="ingredients.id")
    name = serializers.ReadOnlyField(source="ingredients.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredients.measurement_unit"
    )

    class Meta:
        model = IngredientRecipe
        fields = ("id", "name", "measurement_unit", "amount")


class TagSerializer(serializers.ModelSerializer):
    """Обрабатывает эндпоинт /api/tags/"""
    class Meta:
        model = Tag
        fields = (
            'id', 'name', 'color', 'slug'
        )


class RecipeSerializer(serializers.ModelSerializer):
    """Обрабатывает запросы на чтение на эндпоинт /api/recipes/"""
    image = Base64ImageField(required=False, allow_null=True)
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(many=False, read_only=True)
    ingredients = IngredientRecipeSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        """Если рецепт в избранных, вернет True"""
        request = self.context.get('request')
        if request.user.is_anonymous or request is None:
            return False
        return Favorite.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        """Если рецепт в списке покупок, вернет True"""
        request = self.context.get('request')
        if request.user.is_anonymous or request is None:
            return False
        return ShoppingCart.objects.filter(
            user=request.user,
            recipe=obj
        ).exists()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )


class CreateIngredientRecipeSerializer(serializers.ModelSerializer):
    """Обрабатывает данные для 2ух моделей. Таким образом,
    к ингредиентам добавляется поле "amount". Используется для POST запросов
    на создание рецепта."""
    id = serializers.PrimaryKeyRelatedField(
        source='ingredients', queryset=Ingredient.objects.all()
    )

    class Meta:
        model = IngredientRecipe
        fields = ("id", "amount")


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Служит для создания рецептов"""
    image = Base64ImageField(required=True, allow_null=True)
    tags = serializers.ListField(required=True)
    ingredients = CreateIngredientRecipeSerializer(required=True, many=True)

    def to_representation(self, value):
        """Отклик на POST запрос обрабатывается другим сериализатором"""
        return RecipeSerializer(
            value,
            context={'request': self.context.get('request')}
        ).data

    def create(self, validated_data):
        tag_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        recipes = Recipe.objects.create(**validated_data)
        recipes.tags.set(tag_data)
        for ingredient in ingredients_data:
            current_ingredient, status = (
                IngredientRecipe.objects.get_or_create(**ingredient)
            )
            recipes.ingredients.add(current_ingredient)
        return recipes

    def update(self, instance, validated_data):
        tag_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        if validated_data.get('image') is not None:
            instance.image = validated_data.pop('image')
        instance.name = validated_data.pop('name')
        instance.text = validated_data.pop('text')
        instance.cooking_time = validated_data.pop('cooking_time')
        recipes = instance
        recipes.tags.set(tag_data)
        recipes.ingredients.clear()
        for ingredient in ingredients_data:
            current_ingredient, status = (
                IngredientRecipe.objects.get_or_create(**ingredient)
            )
            recipes.ingredients.add(current_ingredient)
        recipes.save()
        return recipes

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )
