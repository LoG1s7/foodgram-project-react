import re

from django.core.exceptions import ValidationError


def validate_name(value):
    pattern = re.compile(r'^[\d\W]+$')
    if pattern.match(value):
        raise ValidationError(
            'Name should not contain only digits and special characters')
