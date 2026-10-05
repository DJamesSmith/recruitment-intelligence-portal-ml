from django.http import HttpRequest
from accounts.models import User


def is_admin_or_hr(request: HttpRequest) -> bool:
    user: User = request.user
    return bool(user.is_authenticated and (user.is_superuser or user.role in {User.Role.ADMIN, User.Role.HR}))


def is_interviewer(request: HttpRequest) -> bool:
    user: User = request.user
    return bool(user.is_authenticated and (user.is_superuser or user.role == User.Role.INTERVIEWER))


def is_staff_role(request: HttpRequest) -> bool:
    user: User = request.user
    return bool(user.is_authenticated and (user.is_superuser or user.role in User.Role.values))
