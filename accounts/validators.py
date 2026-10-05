import re
from django.core.exceptions import ValidationError


EMAIL_PATTERN: re.Pattern[str] = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_PATTERN: re.Pattern[str] = re.compile(r"^\+?[0-9]{10,15}$")


def validate_email_format(value: str) -> None:
    if not EMAIL_PATTERN.fullmatch(value.strip()):
        raise ValidationError("Enter a valid email address.")


def validate_phone_format(value: str) -> None:
    if value and not PHONE_PATTERN.fullmatch(value.strip()):
        raise ValidationError("Enter a valid phone number.")