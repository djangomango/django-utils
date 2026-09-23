import logging
from io import BytesIO
from pathlib import Path
from typing import Any
from uuid import uuid4

import requests
from django.core.files import File
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone

from .requests import get_agent_head_or_default

logger = logging.getLogger(__name__)


def get_object_or_none(model: Any, **kwargs: Any) -> Any:
    """Return the object that matches the keyword arguments or None if not found."""
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None


def get_object_or_404_json(model: Any, **kwargs: Any) -> Any:
    """Return the object matching keyword arguments or a 404 JSON response."""
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return JsonResponse({"error": f"{model.__name__} not found."}, status=404)


def get_all_related_objects(model: Any) -> list[Any]:
    """Return all reverse foreign-key and one-to-one related field descriptors for model."""
    return [
        f
        for f in model._meta.get_fields()
        if (f.one_to_many or f.one_to_one) and f.auto_created and not f.concrete
    ]


def get_all_related_m2m_objects(model: Any) -> list[Any]:
    """Return all reverse many-to-many related field descriptors for model."""
    return [
        f
        for f in model._meta.get_fields(include_hidden=True)
        if f.many_to_many and f.auto_created
    ]


def get_upload_path(instance: Any, filename: str) -> str:
    """Construct a date- and UUID-partitioned storage path for an uploaded model file."""
    path = (
        Path(instance._meta.app_label)
        / instance._meta.model_name
        / timezone.now().strftime("%Y")
        / timezone.now().strftime("%m")
        / uuid4().hex
        / filename
    )

    return str(path).replace("\\", "/")


def check_storage_file_exists(file_path: str, storage: Any = default_storage) -> bool:
    """Check whether a file exists in the designated storage backend."""
    return bool(storage.exists(file_path))


def remove_storage_file_if_exists(
    file_path: str, storage: Any = default_storage
) -> None:
    """Remove the file from storage backend if it currently exists."""
    if check_storage_file_exists(file_path, storage):
        try:
            storage.delete(file_path)
        except Exception as e:
            logger.error(e)


def get_url_as_field_file_or_false(url: str, filename: str) -> Any:
    """Download remote file via HTTP streaming and return in-memory Django File."""
    head = get_agent_head_or_default()
    req = requests.get(url, allow_redirects=True, stream=True, headers=head, timeout=10)
    req.raw.decode_content = True

    if req.status_code == 200:
        bytes_io = BytesIO()
        bytes_io.write(req.content)
        return File(bytes_io, name=filename)

    return False


def render_template(template_name: str, context: dict[str, Any] | None = None) -> str:
    """Render Django template to string with provided context mapping."""
    if context is None:
        context = {}
    return render_to_string(template_name, context=context)


def model_to_dict(
    instance: Any,
    fields: list[str] | tuple[str, ...] | None = None,
    exclude: list[str] | tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """Serialize Django model instance fields to a dictionary."""
    opts = instance._meta
    data = {}
    for f in opts.fields:
        if fields and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        data[f.name] = f.value_from_object(instance)
    return data


def get_user_permission_level(user: Any, obj: Any) -> str | None:
    """Determine highest permission level ('full', 'edit', 'view') user has on object."""
    permission = None
    if user.is_superuser:
        permission = "full"
    elif user.has_perm(f"app.change_{obj.__class__.__name__.lower()}"):
        permission = "edit"
    elif user.has_perm(f"app.view_{obj.__class__.__name__.lower()}"):
        permission = "view"
    return permission
