import re
from collections.abc import Callable

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse


class MaintenanceModeMiddleware:
    """Middleware intercepting non-staff requests during maintenance mode."""

    allowed_patterns: list[str] = [
        r"^/admin/",
        r"^/static/",
        r"^/account/login/$",
        r"^/maintenance/$",
    ]

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        """Initialize middleware with the next request handler."""
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Process incoming request and redirect to maintenance page when required."""
        if not self.pass_request(request):
            match = False
            for pattern in self.allowed_patterns:
                if re.compile(pattern).match(request.path):
                    match = True
                    break

            if not match:
                return redirect(reverse("maintenance"))

        return self.get_response(request)

    @staticmethod
    def pass_request(request: HttpRequest) -> bool:
        """Check if request is authorized to bypass maintenance mode."""
        if request.user.is_authenticated:
            return bool(request.user.is_active and request.user.is_staff)

        return False
