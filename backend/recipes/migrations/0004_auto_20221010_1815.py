# Generated by Django 2.2.19 on 2022-10-10 15:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20221010_1758'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='user',
            new_name='author',
        ),
    ]
