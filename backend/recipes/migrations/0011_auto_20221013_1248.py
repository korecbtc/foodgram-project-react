# Generated by Django 2.2.19 on 2022-10-13 09:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_auto_20221013_0022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author_of_recipe', to=settings.AUTH_USER_MODEL),
        ),
    ]
