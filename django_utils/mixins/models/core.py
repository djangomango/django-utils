from typing import Any

from django.db import models

from ...helpers.django import remove_storage_file_if_exists


class QuerySetByInstanceDelete(models.QuerySet):
    """QuerySet that deletes instances by instance.delete() instead of queryset.delete()"""

    def delete(self, *args: Any, **kwargs: Any) -> Any:
        for obj in self:
            obj.delete()

        return super().delete(*args, **kwargs)


class RemoveFieldFileOnDeleteMixin(models.Model):
    """
    Mixin that removes the file associated with a FileField when a model instance is deleted.

    To use this mixin, simply include it as a mixin in your model class that has FileField(s). The `objects` attribute of
    the model should use the `QuerySetByInstanceDelete` manager as its manager.

    Example usage:

    class MyModel(RemoveFieldFileOnDeleteMixin, models.Model):
        myfile = models.FileField()

        objects = QuerySetByInstanceDelete.as_manager()
    """

    objects = QuerySetByInstanceDelete.as_manager()

    class Meta:
        abstract = True

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.filefields_to_remove_on_delete = [
            field.name for field in self._meta.fields
        ]

    def delete(self, using: Any = None, keep_parents: bool = False) -> Any:
        for field_name in self.filefields_to_remove_on_delete:
            field = getattr(self, field_name, None)
            remove_storage_file_if_exists(field.name)

        return super().delete()


class RemoveFieldFileOnChangeMixin(models.Model):
    """Mixin that removes the file associated with a FileField when a model instance is saved and the field has changed."""

    _stored: dict

    class Meta:
        abstract = True

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.filefields_to_remove_on_change = [
            field.name for field in self._meta.fields
        ]

    @classmethod
    def from_db(cls, db: Any, field_names: Any, values: Any) -> Any:
        instance = super().from_db(db, field_names, values)
        instance._stored = dict(zip(field_names, values, strict=False))
        return instance

    def save(self, *args: Any, **kwargs: Any) -> None:

        if not self._state.adding:
            for field_name in self.filefields_to_remove_on_change:
                field = getattr(self, field_name, None)
                stored_field = (
                    self._stored.pop(field_name, None)
                    if hasattr(self, "_stored")
                    else None
                )

                if field != stored_field:
                    remove_storage_file_if_exists(stored_field)

        super().save(*args, **kwargs)
