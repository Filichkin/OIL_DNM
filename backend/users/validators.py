import re

from django.core.exceptions import ValidationError


def validate_dealer_code(rs_code):
    if not re.fullmatch(r'RS\d{3}', rs_code):
        raise ValidationError(
            'Код дилера должен состоять из RS и трех цифр'
        )
    return rs_code


def validate_inn(inn):
    if not inn.is_integer() and not len(str(inn)) in (10, 12):
        raise ValidationError(
            'ИНН должен состоять из 10 или 12 цифр'
        )
    return inn
