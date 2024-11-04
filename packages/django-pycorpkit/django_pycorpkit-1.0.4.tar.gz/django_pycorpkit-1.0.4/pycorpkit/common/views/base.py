from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied


class BaseViewSet(viewsets.ModelViewSet):

    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            data = kwargs["data"]
            if isinstance(data, list):
                kwargs["many"] = True
        return super(BaseViewSet, self).get_serializer(*args, **kwargs)


class RequiresOrganisation(permissions.BasePermission):
    """
    Permission class to enforce organisation_id requirement
    """
    message = "Organisation ID is required in headers"

    def has_permission(self, request, view):
        if not request.organisation_id:
            return False
        if not request.organisation:
            raise PermissionDenied("Invalid organisation ID provided")
        return True


class OrganisationViewSet(viewsets.ModelViewSet):
    """
    Base ViewSet for organisation-specific views.
    Includes organisation permission and filtering by default.
    """
    permission_classes = [RequiresOrganisation]

    def get_queryset(self):
        """
        Filter queryset by organisation_id by default
        """
        queryset = super().get_queryset()
        return queryset.filter(organisation=self.request.organisation_id)

    def perform_create(self, serializer):
        """
        Automatically set organisation when creating objects
        """
        serializer.save(organisation=self.request.organisation)
