# Generated by Django 2.2.19 on 2022-10-16 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0019_auto_20221016_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(blank=True, max_length=200, unique=True, verbose_name='Name of recipe'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='text',
            field=models.CharField(blank=True, max_length=2000, verbose_name='Description'),
        ),
    ]
