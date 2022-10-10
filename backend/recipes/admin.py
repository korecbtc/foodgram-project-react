from django.contrib import admin
from .models import Tag, Ingredient, Recipe, Favotite, IngredientRecipe

admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Favotite)
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
        return obj.favorite_recipe.count()
