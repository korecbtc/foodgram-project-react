# Generated by Django 2.2.19 on 2022-10-16 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0020_auto_20221016_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Name of recipe'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='text',
            field=models.CharField(max_length=2000, verbose_name='Description'),
        ),
    ]
