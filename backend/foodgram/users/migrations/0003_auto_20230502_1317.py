# Generated by Django 3.2 on 2023-05-02 13:17

from django.db import migrations, models

import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20230502_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=150, validators=[users.validators.validate_first_name], verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=150, validators=[users.validators.validate_first_name], verbose_name='Фамилия'),
        ),
    ]
