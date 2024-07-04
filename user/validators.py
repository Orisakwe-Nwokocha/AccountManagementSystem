from django.core.exceptions import ValidationError


def validate_phone_number(phone_number: str):
    if len(phone_number) < 11 or not phone_number.isdigit():
        raise ValidationError('Enter a valid 11 digit number')
