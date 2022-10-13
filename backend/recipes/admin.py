from django.contrib import admin
from .models import Tag, Ingredient, Recipe, Favorite, IngredientRecipe
from .models import ShoppingCart

admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(IngredientRecipe)
admin.site.register(ShoppingCart)
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
        return obj.in_favorite.count()


@admin.register(Ingredient)
class Ingredient(admin.ModelAdmin):
    list_filter = ('name',)
    list_display = (
        'name',
        'measurement_unit'
    )
