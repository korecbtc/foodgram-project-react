from django.contrib import admin
from .models import Tag, Ingredient, Recipe, Favorite, IngredientRecipe
from .models import ShoppingCart

admin.site.register(Tag)
admin.site.register(IngredientRecipe)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_filter = ('author', 'name', 'tags')
    list_display = (
        'name',
        'author',
        'cooking_time',
        'show_favorite_count'
    )

    def show_favorite_count(self, obj):
        """Счетчик добавления в избранное"""
        return obj.is_favorited.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    list_display = (
        'name',
        'measurement_unit'
    )


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'user'
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'user'
    )
