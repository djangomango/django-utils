class TimeStampAdminMixin:
    """Admin mixin exposing created_at and modified_at timestamp fields."""

    list_display = [
        "created_at",
        "modified_at",
    ]

    fields = [
        "created_at",
        "modified_at",
    ]

    readonly_fields = [
        "created_at",
        "modified_at",
    ]


class UuidAdminMixin:
    """Admin mixin displaying read-only uuid field."""

    list_display = []

    fields = [
        "uuid",
    ]

    readonly_fields = [
        "uuid",
    ]


class OrderAdminMixin:
    """Admin mixin managing order positioning field."""

    list_display = [
        "order",
    ]

    fields = [
        "order",
    ]

    readonly_fields = []


class TitleAdminMixin:
    """Admin mixin configuring title field display."""

    list_display = [
        "title",
    ]

    fields = [
        "title",
    ]

    readonly_fields = []


class TitleSlugAdminMixin:
    """Admin mixin displaying title and read-only slug fields."""

    list_display = [
        "title",
    ]

    fields = [
        "title",
        "slug",
    ]

    readonly_fields = [
        "slug",
    ]


class DescriptionAdminMixin:
    """Admin mixin configuring description field."""

    list_display = []

    fields = [
        "description",
    ]

    readonly_fields = []


class BodyAdminMixin:
    """Admin mixin configuring body content field."""

    list_display = []

    fields = [
        "body",
    ]

    readonly_fields = []


class BodyExcerptAdminMixin:
    """Admin mixin configuring body, short excerpt, and long excerpt fields."""

    list_display = []

    fields = [
        "body",
        "excerpt_short",
        "excerpt_long",
    ]

    readonly_fields = []


class PositionAdminMixin:
    """Admin mixin configuring job/role position field."""

    list_display = [
        "position",
    ]

    fields = [
        "position",
    ]

    readonly_fields = []

