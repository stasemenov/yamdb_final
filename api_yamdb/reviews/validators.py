import datetime as dt

from django.core.exceptions import ValidationError


def validate_year(value):
    year = dt.date.today().year
    if value > year:
        raise ValidationError('Год не может быть больше текущего.')
    return value
