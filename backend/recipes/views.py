from django.shortcuts import render
from rest_framework import viewsets
from .models import Ingredient, Tag, Recipe, Favorite, ShoppingCart, IngredientRecipe
from .serializers import IngredientSerializer, TagSerializer
from .serializers import RecipeSerializer, RecipeCreateSerializer
from .serializers import ShoppingCartSerializer
from api.pagination import LimitPageNumberPagination
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view


@api_view(['GET'])
def download(request):
    # ingredients = IngredientRecipe.objects.filter(
    #         recipe__purchases__user=request.user
    #     )
    list_of_obj = get_list_or_404(ShoppingCart, user=request.user)
    list_of_ingredients =[]
    list_of_recipes = []
    ingredients = []
    ingredients_measure = {}
    ingredients_amount = {}
    count = 0
    for shop in list_of_obj:
        list_of_recipes.append(shop.recipe)

    list_of_ingredients = (IngredientRecipe.objects.filter(recipe__in=list_of_recipes))
    amount = list(list_of_ingredients.values_list('amount', flat=True))
    ingredients_ids = list(list_of_ingredients.values_list('ingredients', flat=True))
    for ingredient_id in ingredients_ids:
        ingredient = Ingredient.objects.get(pk=ingredient_id)
        ingredients.append(ingredient.name)
        if ingredient.name not in ingredients_amount.keys():
            ingredients_amount[ingredient.name] = amount[count]
            ingredients_measure[ingredient.name] = ingredient.measurement_unit
        else:
            ingredients_amount[ingredient.name] += amount[count]
        count += 1
    print(amount, ingredients, ingredients_amount, ingredients_measure)


class ShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get('recipe_id'))
        serializer.save(user=self.request.user, recipe=recipe)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def get_queryset(self):
        """Обработка GET запроса с параметром"""
        ingredient = self.request.query_params.get("name", None)
        if ingredient:
            return Ingredient.objects.filter(name__startswith=ingredient)
        return super().get_queryset()
     

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    pagination_class = LimitPageNumberPagination
    queryset = Recipe.objects.all()

    def get_queryset(self):
        """Обработка GET запросов с параметрами"""
        favorite = self.request.query_params.get('is_favorited', None)
        shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart', None
        )
        author = self.request.query_params.get('author', None)
        tag = self.request.query_params.getlist('tags')
        if favorite == '1':
            return Recipe.objects.filter(is_favorite__user=self.request.user)
        if shopping_cart == '1':
            return Recipe.objects.filter(
                is_in_shopping_cart__user=self.request.user
            )
        if author:
            return get_list_or_404(Recipe, author_id=author)
        if tag:
            return Recipe.objects.filter(tags__slug__in=tag)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
