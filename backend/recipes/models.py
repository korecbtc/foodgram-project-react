from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=256,
        blank=False,
        unique=True,
        verbose_name='Name of tag',
        )

    color = models.CharField(
        max_length=256,
        blank=False,
        unique=True,
        verbose_name='HEX-color',
        )

    slug = models.SlugField(
        max_length=256,
        blank=False,
        unique=True,
        )
    
    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=256,
        blank=False,
        unique=True,
        verbose_name='Name of ingredient',
        )
    
    measurement_unit = models.CharField(
        max_length=256,
        blank=False,
        unique=True,
        verbose_name='Measurement_unit',
        )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        max_length=200,
        blank=False,
        unique=True,
        verbose_name='Name of recipe',
        )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='author'
    )

    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientRecipe', related_name='recipe'
    )

    tags = models.ForeignKey(
        Tag,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='tags'
    )

    image = models.ImageField(
        upload_to='recipe/images/',
        null=True,
        default=None
        )

    text = models.CharField(
        max_length=2000,
        blank=False,
        unique=False,
        verbose_name='Description',
        )

    cooking_time = models.IntegerField(
        verbose_name='Time of cooking in minutes'
    )

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='ingredient_recipe'
    )

    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='ingredient_recipe'
    )

    quantity = models.IntegerField()


class Favotite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='current_user'
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='favorite_recipe'
    )

    class Meta:
        verbose_name = 'Favorite'
        unique_together = [['user', 'recipe']]

