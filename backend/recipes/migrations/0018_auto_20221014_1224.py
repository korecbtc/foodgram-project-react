# Generated by Django 2.2.19 on 2022-10-14 09:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0017_auto_20221014_1204'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredientrecipe',
            old_name='quantity',
            new_name='amount',
        ),
    ]
