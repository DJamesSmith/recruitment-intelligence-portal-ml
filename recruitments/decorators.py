from collections.abc import Callable
from functools import wraps
from typing import Any

from django.http import HttpRequest, HttpResponse, JsonResponse
from accounts.models import User


def recruitment_access(view: Callable) -> Callable:
    @wraps(view)
    def wrapper(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        user: User = request.user
        if not user.is_authenticated:
            return JsonResponse({"detail": "Authentication required."}, status=401)
        if user.is_superuser or user.role in {User.Role.ADMIN, User.Role.HR, User.Role.INTERVIEWER}:
            return view(request, *args, **kwargs)
        return JsonResponse({"detail": "Permission denied."}, status=403)
    return wrapper