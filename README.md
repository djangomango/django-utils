# Django-Utils

A comprehensive library of reusable helpers, model mixins, form mixins, admin mixins, middleware, and tools designed to streamline Django development.

---

## Installation

```bash
pip install git+https://github.com/djangomango/django-utils.git@0.1.0
```

Or add to your `requirements.txt`:

```txt
git+https://github.com/djangomango/django-utils.git@0.1.0
```

Or clone directly as a submodule into your project's `utils/` directory:

```bash
git submodule add https://github.com/djangomango/django-utils.git path/to/project/utils
```

### Optional Dependencies

Install extra dependencies if using MIME validation (`python-magic`) or HTTP utilities (`requests`):

```bash
pip install "django-utils[all] @ git+https://github.com/djangomango/django-utils.git@0.1.0"
```

---

## Usage

### 1. General Helpers

```python
from django_utils.helpers.dict import deep_merge
from django_utils.helpers.string import slugify_unique
from django_utils.helpers.file import get_file_extension

# Deep merge configuration dictionaries
merged_dict = deep_merge(base_defaults, user_overrides)

# Generate unique slug for model
slug = slugify_unique(Article, "title", "My Blog Post")
```

### 2. Model Mixins

```python
from django.db import models
from django_utils.mixins.models import TimestampMixin, UUIDPrimaryKeyMixin


class BlogPost(UUIDPrimaryKeyMixin, TimestampMixin, models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
```

### 3. Middleware

Add utility middleware in `settings.py`:

```python
MIDDLEWARE = [
    ...
    "django_utils.middleware.SecurityHeadersMiddleware",
    "django_utils.middleware.HTMLMinifyMiddleware",
    ...
]
```

---

## License & Credits

- Licensed under the **GNU Lesser General Public License v3 (LGPLv3)**.