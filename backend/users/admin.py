from django.contrib import admin

from .models import User, Follow


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ('email', 'username')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'following'
    )