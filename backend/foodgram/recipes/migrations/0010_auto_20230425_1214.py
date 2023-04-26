# Generated by Django 3.2 on 2023-04-25 12:14

from django.db import migrations, models
import recipes.validators


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_auto_20230425_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=200, validators=[recipes.validators.validate_name], verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=200, validators=[recipes.validators.validate_name], verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=200, validators=[recipes.validators.validate_name], verbose_name='Название'),
        ),
    ]
