import django_filters
from django.core.exceptions import FieldError
from django.db.models import Case, IntegerField, Value, When
from rest_framework import filters


class BaseFilter(django_filters.FilterSet):
    """Default base filter for all filters, includes select-boxes and search."""

    def selectbox_filter(self, queryset, field, value):
        """Ensure that selectbox search results include the selected item."""
        ordering_filters = ("custom_order", "-updated", "-created")
        return queryset.annotate(
            custom_order=Case(
                When(pk=value, then=Value(0)),
                output_field=IntegerField(),
                default=Value(1),
            )
        ).order_by(*(ordering_filters))

    selectbox = django_filters.UUIDFilter(method="selectbox_filter")


class OrganisationFilterBackend(filters.BaseFilterBackend):
    """
    Users are only allowed to view records thier organisation.
    """

    def filter_queryset(self, request, queryset, view):
        """Filter all records based on a users organisation."""
        try:
            return queryset.filter(organisation_id=request.organisation_id)
        except FieldError:
            return queryset
