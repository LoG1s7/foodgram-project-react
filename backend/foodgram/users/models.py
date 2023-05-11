from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from recipes.validators import validate_name
from users.validators import validate_me_name


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
            'Необходимое поле. 150 или менее символов. '
            'Только буквы, цифры и эти символы: "@/./+/-/_" .'),
        validators=[username_validator, validate_me_name],
        error_messages={
            'unique': "Пользователь с таким именем уже существует",
        },
    )
    first_name = models.CharField(
        'Имя',
        max_length=settings.USER_LEN_NAME,
        validators=(validate_name, )
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=settings.USER_LEN_NAME,
        validators=(validate_name, )
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
