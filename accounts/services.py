from datetime import datetime, timedelta
import secrets

import jwt
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from accounts.models import EmailOTP, User


def create_verification_code(user: User) -> EmailOTP:
    code: str = str(secrets.randbelow(900000) + 100000)
    otp: EmailOTP = EmailOTP.objects.create(user=user, code=code, expires_at=timezone.now() + timedelta(minutes=10))
    send_mail("Email verification code", f"Your verification code is {code}.", None, [user.email])
    return otp


def verify_code(user: User, code: str) -> bool:
    otp: EmailOTP | None = EmailOTP.objects.filter(user=user, code=code, is_used=False, expires_at__gte=timezone.now()).first()
    if otp is None:
        return False
    otp.is_used = True
    otp.save(update_fields=["is_used"])
    user.is_email_verified = True
    user.save(update_fields=["is_email_verified"])
    return True


def create_token(user: User, days: int = 1) -> str:
    now: datetime = timezone.now()
    payload: dict[str, object] = {
        "user_id": user.id,
        "email": user.email,
        "role": user.role,
        "exp": now + timedelta(days=days),
        "iat": now,
    }
    return str(jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256"))


def decode_token(token: str) -> dict[str, object]:
    return dict(jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"]))
