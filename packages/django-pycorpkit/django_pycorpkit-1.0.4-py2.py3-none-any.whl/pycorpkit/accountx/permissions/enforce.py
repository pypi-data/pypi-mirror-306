from django.core.exceptions import ImproperlyConfigured
from rest_framework import permissions


class EnforceDRFViewPermission(permissions.BasePermission):
    """This is what is responsible of enforcing or checking permissions in views."""

    perm_attr_name = "permissions"

    def _flatten_perm_list(self, perm_list):
        """
        Recursively flattens a list of permissions,
        ensuring each permission is either a tuple or a list.
        """
        if perm_list is None:
            return []
        flattened_perms = []
        for perm in perm_list:
            if isinstance(perm, tuple):
                flattened_perms.append(perm[0])
            elif isinstance(perm, list):
                flattened_perms.extend(self._flatten_perm_list(perm))
            else:
                raise ImproperlyConfigured(
                    "Permissions should be either a tuple or a list"
                )
        return flattened_perms

    def _get_method_perms(self, method, perm_dict):
        """
        Retrieves permissions based on HTTP method.
        Handles fallback for OPTIONS, HEAD, and PUT methods.
        """
        method = method.upper()
        perms = perm_dict.get(method)
        if method in {"OPTIONS", "HEAD"}:
            perms = perms or perm_dict.get("GET")
        elif method == "PUT":
            perms = perms or perm_dict.get("PATCH")

        if perms is not None and not isinstance(perms, list):
            raise ImproperlyConfigured("HTTP `method` permissions should be a list")

        return perms or []

    def _process_perms(self, request, view_perms):
        """
        Validates if the user's permissions include those required by the view.
        """
        method = request.method
        perms = self._flatten_perm_list(self._get_method_perms(method, view_perms))
        return request.user.has_permissions(perms, request.organisation_id)

    def get_perms(self, request, view):
        """
        Retrieves the permissions attribute from the view.
        """
        return getattr(view, self.perm_attr_name, None)

    def has_permission(self, request, view):
        """
        Main entry point for determining whether the request
        has the necessary permissions.
        If the view does not specify the permissions at all, it means
        that view is not wrapped with authorization for all HTTP requests.
        If the permissions defined in the view don't include a specific.
        HTTP request method it means authorization is not required for that
        HTTP method and there is no need to check and enforce permissions
        for that HTTP method.
        """
        view_perms = self.get_perms(request, view)
        if view_perms is None:
            return True

        if not isinstance(view_perms, dict):
            raise ImproperlyConfigured("Permissions should be a dict.")

        http_methods = list(view_perms.keys())
        if request.method not in http_methods:
            return True

        return self._process_perms(request, view_perms)
