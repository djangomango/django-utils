import csv
from typing import Any

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse


class NoAddAdminMixin:
    """ModelAdmin mixin disabling add action permissions."""

    extra = 0
    max_num = 0

    @staticmethod
    def has_add_permission(request: HttpRequest, obj: Any = None) -> bool:
        """Deny add permission."""
        return False


class NoDeleteAdminMixin:
    """ModelAdmin mixin disabling delete action permissions."""

    @staticmethod
    def has_delete_permission(request: HttpRequest, obj: Any = None) -> bool:
        """Deny delete permission."""
        return False


class NoAddDeleteAdminMixin(NoAddAdminMixin):
    """ModelAdmin mixin disabling both add and delete action permissions."""

    @staticmethod
    def has_delete_permission(request: HttpRequest, obj: Any = None) -> bool:
        """Deny delete permission."""
        return False


class NoModuleAdminMixin:
    """ModelAdmin mixin disabling admin module index view permissions."""

    @staticmethod
    def has_module_permission(request: HttpRequest, obj: Any = None) -> bool:
        """Deny module permission."""
        return False


class ExportCsvMixin(admin.ModelAdmin):
    """ModelAdmin mixin adding CSV export action for change list views."""

    def __init__(self, model: Any, admin_site: Any) -> None:
        """Register CSV export action on ModelAdmin initialization."""
        super().__init__(model, admin_site)

        if "export_as_csv" not in self.actions:
            self.actions += ("export_as_csv",)

    def export_as_csv(
        self, request: HttpRequest, queryset: QuerySet[Any]
    ) -> HttpResponse:
        """Export selected queryset rows to a downloaded CSV file."""
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename={meta}.csv"
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"
