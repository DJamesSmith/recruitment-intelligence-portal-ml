from django.core.exceptions import ValidationError


def validate_non_negative(value: int | float) -> None:
    if value < 0:
        raise ValidationError("Value cannot be negative.")