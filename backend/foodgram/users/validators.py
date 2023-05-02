from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _


def validate_first_name(value):
    if not value.isalpha():
        raise ValidationError(
            _("Имя должно состоять только из букв"),
        )
    if not value[0].isupper():
        raise ValidationError(
            _("Имя начинается с заглавной буквы"),
        )


def validate_last_name(value):
    if not value.isalpha():
        raise ValidationError(
            _("Фамилия должна состоять только из букв"),
        )
    if not value[0].isupper():
        raise ValidationError(
            _("Фамилия начинается с заглавной буквы"),
        )


def validate_me_name(username):
    if username.lower() == 'me':
        raise ValidationError(f'Некорректное имя пользователя {username}')
    return username
