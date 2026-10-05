import logging
import time
from collections.abc import Callable

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from accounts.models import User

logger: logging.Logger = logging.getLogger(__name__)


class RequestLogMiddleware:
    def __init__(self: "RequestLogMiddleware", get_response: Callable) -> None:
        self.get_response: Callable = get_response

    def __call__(self: "RequestLogMiddleware", request: HttpRequest) -> HttpResponse:
        start: float = time.perf_counter()
        user: User = request.user
        role: str = getattr(user, "role", "anonymous")

        if request.path.startswith("/recruitments/dashboard/") and not user.is_authenticated:
            response: HttpResponse = redirect("login")
        else:
            response = self.get_response(request)

        elapsed: float = time.perf_counter() - start
        logger.info("%s %s %.4fs role=%s", request.method, request.path, elapsed, role)
        return response
