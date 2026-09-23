from typing import Any

from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMixin:
    """Redirects to the login page if the user is not authenticated."""

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login") + "?next=" + request.path)
        return super().dispatch(request, *args, **kwargs)


class SuperuserRequiredMixin:
    """Redirects to the login page if the user is not authenticated or is not a superuser."""

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated or not request.user.is_superuser:
            return HttpResponseRedirect(reverse("login") + "?next=" + request.path)
        return super().dispatch(request, *args, **kwargs)


class PermissionRequiredMixin:
    """Redirects to the permission denied page if the user does not have the required permission."""

    permission_required = None

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.has_perm(self.permission_required):
            return HttpResponseRedirect(reverse("permission_denied_url"))
        return super().dispatch(request, *args, **kwargs)


class SuccessMessageMixin:
    """Add a success message on successful form submission."""

    success_message = None

    def form_valid(self, form: Any) -> HttpResponse:
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response

    def get_success_message(self, cleaned_data: Any) -> Any:
        """Return the configured success message."""
        return self.success_message

    def get_success_url(self) -> str:
        return reverse("success_url")


class NextUrlMixin:
    """Mixin that redirects to the next URL after a form submission."""

    default_next = "/"

    def get_next_url(self) -> str:
        """Resolve redirect URL from request parameters or fallback default."""
        next_url = self.request.GET.get("next") or self.request.POST.get("next")
        return next_url or self.default_next

    def form_valid(self, form: Any) -> HttpResponse:
        super().form_valid(form)
        return redirect(self.get_next_url())
