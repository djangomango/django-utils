from .atoms import (
    BodyAdminMixin,
    BodyExcerptAdminMixin,
    DescriptionAdminMixin,
    OrderAdminMixin,
    PositionAdminMixin,
    TitleAdminMixin,
)


class PageAdminMixin(DescriptionAdminMixin):
    """Admin mixin combining description and summary fields for page models."""

    list_display = [*DescriptionAdminMixin.list_display]

    fields = [*DescriptionAdminMixin.fields, "summary"]

    readonly_fields = [*DescriptionAdminMixin.readonly_fields]


class ContentAdminMixin(
    OrderAdminMixin, TitleAdminMixin, BodyAdminMixin, PositionAdminMixin
):
    """Admin mixin combining order, title, body, and position for content blocks."""

    list_display = (
        OrderAdminMixin.list_display
        + TitleAdminMixin.list_display
        + BodyAdminMixin.list_display
        + PositionAdminMixin.list_display
        + []
    )

    fields = (
        OrderAdminMixin.fields
        + TitleAdminMixin.fields
        + BodyAdminMixin.fields
        + PositionAdminMixin.fields
        + []
    )

    readonly_fields = (
        OrderAdminMixin.readonly_fields
        + TitleAdminMixin.readonly_fields
        + BodyAdminMixin.readonly_fields
        + PositionAdminMixin.readonly_fields
        + []
    )


class FeatureAdminMixin(OrderAdminMixin, TitleAdminMixin, BodyAdminMixin):
    """Admin mixin combining order, title, body, and featured flag for highlights."""

    list_display = (
        OrderAdminMixin.list_display
        + TitleAdminMixin.list_display
        + BodyAdminMixin.list_display
        + [
            "featured",
        ]
    )

    fields = (
        OrderAdminMixin.fields
        + TitleAdminMixin.fields
        + BodyAdminMixin.fields
        + [
            "featured",
        ]
    )

    readonly_fields = (
        OrderAdminMixin.readonly_fields
        + TitleAdminMixin.readonly_fields
        + BodyAdminMixin.readonly_fields
        + []
    )


class DocumentAdminMixin(TitleAdminMixin, BodyAdminMixin):
    """Admin mixin combining title, body, datetime, published, and featured for docs."""

    list_display = (
        TitleAdminMixin.list_display
        + BodyAdminMixin.list_display
        + [
            "datetime",
            "published",
            "featured",
        ]
    )

    fields = (
        TitleAdminMixin.fields
        + BodyAdminMixin.fields
        + [
            "datetime",
            "published",
            "featured",
        ]
    )

    readonly_fields = (
        TitleAdminMixin.readonly_fields + BodyAdminMixin.readonly_fields + []
    )


class PostAdminMixin(TitleAdminMixin, BodyExcerptAdminMixin):
    """Admin mixin combining title, excerpt body, datetime, published, and featured for posts."""

    list_display = (
        TitleAdminMixin.list_display
        + BodyExcerptAdminMixin.list_display
        + [
            "datetime",
            "published",
            "featured",
        ]
    )

    fields = (
        TitleAdminMixin.fields
        + BodyExcerptAdminMixin.fields
        + [
            "datetime",
            "published",
            "featured",
        ]
    )

    readonly_fields = (
        TitleAdminMixin.readonly_fields + BodyExcerptAdminMixin.readonly_fields + []
    )
