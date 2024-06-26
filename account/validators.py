from django.core.exceptions import ValidationError


def validate_pin(pin: str):
    if len(pin) < 4 or not pin.isdigit():
        raise ValidationError('Pin must be at least four digits')