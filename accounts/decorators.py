from collections.abc import Callable
from functools import wraps

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from accounts.models import User


def role_required(*roles: str) -> Callable:
    def decorator(view: Callable) -> Callable:
        @wraps(view)
        def wrapper(request: HttpRequest, *args, **kwargs) -> HttpResponse:
            user: User = request.user
            if not user.is_authenticated:
                return redirect("login")
            if not (user.is_superuser or user.role in roles):
                return HttpResponse("Permission denied.", status=403)
            return view(request, *args, **kwargs)
        return wrapper
    return decorator