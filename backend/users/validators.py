import re

from django.core.exceptions import ValidationError


def validate_dealer_code(rs_code):
    if re.fullmatch(r'RS\d{3}', rs_code):
        raise ValidationError(
            'Код дилера должен состоять из RS и трех цифр'
        )
    return rs_code


def validate_inn(inn):
    if re.fullmatch(r'\d{12}', inn):
        raise ValidationError(
            'ИНН должен состоять из 12 цифр'
        )
    return inn
