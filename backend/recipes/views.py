from django.shortcuts import render
from rest_framework import viewsets
from .models import Ingredient, Tag, Recipe, Favorite
from .serializers import IngredientSerializer, TagSerializer
from .serializers import RecipeSerializer, RecipeCreateSerializer
from api.pagination import LimitPageNumberPagination
from django.shortcuts import get_list_or_404


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def get_queryset(self):
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
    serializer_class = RecipeSerializer

    def get_queryset(self):
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
