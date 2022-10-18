from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Ingredient, Tag, Recipe, Favorite, ShoppingCart, IngredientRecipe
from .serializers import IngredientSerializer, TagSerializer
from .serializers import RecipeSerializer, RecipeCreateSerializer
from .serializers import ShoppingCartSerializer
from api.pagination import LimitPageNumberPagination
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import HttpResponse


@api_view(['GET'])
def download_shopping_cart(request):
    ingredients = IngredientRecipe.objects.filter(
            recipe__is_in_shopping_cart__user=request.user
        )
    shopping_dict = {}
    data = ''
    for ingredient in ingredients:
        amount = ingredient.amount
        name = ingredient.ingredients.name
        measurement_unit = ingredient.ingredients.measurement_unit
        if name not in shopping_dict:
            shopping_dict[name] = {
                'amount': amount,
                'measurement_unit': measurement_unit
            }
        else:
            shopping_dict[name]['amount'] += amount
    for ingredient in shopping_dict:
        data += ingredient + ' - ' + str(
            shopping_dict[ingredient]['amount']
            ) + ' ' + shopping_dict[ingredient]['measurement_unit'] + '\n'
    return HttpResponse(data, content_type='text/plain')


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """Обработка запросов на добавление/удаление из списка покупок"""
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get('recipes_id'))
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save(user=self.request.user, recipe=recipe)

    def destroy(self, request, recipes_id):
        instance = get_object_or_404(ShoppingCart, recipe=recipes_id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


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
