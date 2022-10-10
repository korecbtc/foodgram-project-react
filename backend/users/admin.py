from django.contrib import admin

from .models import User, Follow

admin.site.register(Follow)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ('email', 'username')
