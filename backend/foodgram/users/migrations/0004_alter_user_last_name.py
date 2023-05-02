# Generated by Django 3.2 on 2023-05-02 13:27

from django.db import migrations, models

import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20230502_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=150, validators=[users.validators.validate_last_name], verbose_name='Фамилия'),
        ),
    ]
