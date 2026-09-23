import random
from pathlib import Path
from typing import Any

import requests
from django.http import HttpRequest


def get_or_create_request_session_key(request: HttpRequest) -> str:
    """Return the session key for the given request."""
    if not request.session.exists(request.session.session_key):
        request.session.create()

    return str(request.session.session_key)


def get_request_remote_addr(request: HttpRequest) -> str:
    """Return the remote address of the given request."""
    x_forwarded_for = request.headers.get("X-Forwarded-For", "")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]

    if not hasattr(request, "META"):
        return ""

    return str(request.META.get("REMOTE_ADDR", ""))


def get_request_ua_string(request: HttpRequest) -> str:
    """Return the user agent string of the given request."""
    if not hasattr(request, "META"):
        return ""

    return str(request.META.get("HTTP_USER_AGENT", ""))


def get_random_agent_or_false() -> str | bool:
    """Return a random user agent string from the user agent list file or False if absent."""
    agent_file = Path(__file__).resolve().parent / "data" / "user_agent_list.txt"
    if agent_file.is_file():
        lines = [
            line.strip()
            for line in agent_file.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        if lines:
            return random.choice(lines)

    return False


def get_agent_head_or_default() -> dict[str, str]:
    """Return the default user agent header or a random user agent header."""
    head = {
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
    }

    agent = get_random_agent_or_false()
    if agent:
        head["User-Agent"] = str(agent)

    return head


def get_url_head_or_false(url: str) -> Any:
    """Return the head of the given URL or False if the request fails."""
    head = get_agent_head_or_default()
    req = requests.head(url, allow_redirects=True, headers=head, timeout=5)
    if req.status_code == requests.codes.ok:
        return req

    return False


def get_client_ip(request: HttpRequest) -> str:
    """Return the client IP address."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    ip = (
        x_forwarded_for.split(",")[0]
        if x_forwarded_for
        else request.META.get("REMOTE_ADDR")
    )
    return str(ip or "")
