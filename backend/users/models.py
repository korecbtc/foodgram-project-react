from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    CHOICES = (
        ('user', 'user'), ('admin', 'admin')
    )
    first_name = models.CharField(
        max_length=150, blank=False, verbose_name='First name'
    )
    last_name = models.CharField(
        max_length=150, blank=False, verbose_name='Last name'
    )
    email = models.EmailField(
        max_length=254,
        blank=False,
        unique=True,
        verbose_name='E-mail',
    )
    role = models.CharField(max_length=150, choices=CHOICES, default='user')
    password = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='Password'
    )
    username = models.CharField(
        max_length=150,
        blank=False,
        unique=True,
        verbose_name='Username'
    )

    @property
    def is_admin(self):
        # Предусмотрена возможность использования роли администратора.
        # В проекте не задействована
        return self.role == 'admin'

    def __str__(self):
        return f'{self.username}'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='follower'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='following'
    )

    class Meta:
        verbose_name = 'Follow'
        unique_together = [['user', 'following']]

    def __str__(self):
        return f'{self.user}'
