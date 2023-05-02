from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from users.validators import (validate_first_name, validate_last_name,
                              validate_me_name)


class User(AbstractUser):

    username_validator = UnicodeUsernameValidator()

    email = models.EmailField(
        'Электронная почта',
        max_length=settings.LEN_EMAIL,
        unique=True
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=settings.USER_LEN_NAME,
        unique=True,
        help_text=(
            'Required. 150 characters or fewer. '
            'Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator, validate_me_name],
        error_messages={
            'unique': ("A user with that username already exists."),
        },
    )
    first_name = models.CharField(
        'Имя',
        max_length=settings.USER_LEN_NAME,
        validators=(validate_first_name, )
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=settings.USER_LEN_NAME,
        validators=(validate_last_name,)
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
