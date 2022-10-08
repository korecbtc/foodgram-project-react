from django.db import models


class Tags(models.Model):
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

    