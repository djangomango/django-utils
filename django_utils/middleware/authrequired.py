import re
from collections.abc import Callable

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse


class AuthRequiredMiddleware:
    """Middleware enforcing authentication across all endpoints except allowed patterns."""

    allowed_patterns: list[str] = [
        r"^/admin/",
        r"^/static/",
        r"^/account/login/$",
        r"^/account/password-reset/$",
        r"^/account/password-reset-done/$",
        r"^/account/password-reset-complete/$",
        r"^/account/password-change-done/$",
        r"^/account/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,36})/$",
        r"^/account/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/set-password/$",
        r"^/maintenance/$",
    ]

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        """Initialize middleware with the next request handler."""
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Process incoming request and redirect to login if authentication is required."""
        if not self.pass_request(request):
            match = False
            for pattern in self.allowed_patterns:
                if re.compile(pattern).match(request.path):
                    match = True
                    break

            if not match:
                return redirect(reverse("account:login"))

        return self.get_response(request)

    @staticmethod
    def pass_request(request: HttpRequest) -> bool:
        """Check if request passes authentication requirements."""
        return bool(request.user.is_authenticated)
