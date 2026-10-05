from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.http import HttpRequest

from accounts.models import User


class EmailBackend(ModelBackend):
    def authenticate(self: "EmailBackend", request: HttpRequest | None, username: str | None = None, password: str | None = None, **kwargs: Any) -> User | None:
        email: str | None = kwargs.get("email", username)
        if not email or not password:
            return None

        user_model: type[User] = get_user_model()
        try:
            user: User = user_model.objects.get(email=email.lower())
        except user_model.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
