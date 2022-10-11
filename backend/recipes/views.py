from django.shortcuts import render
from rest_framework import viewsets
from .models import Ingredient
from .serializers import IngredientSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def get_queryset(self):
        ingredient = self.request.query_params.get("name", None)
        if ingredient:
            return Ingredient.objects.filter(name__startswith=ingredient)
        return super().get_queryset()
             
