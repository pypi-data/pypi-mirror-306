import pytest
from django.urls import reverse
from rest_framework import status


class TestRoleViews:
    def setup_method(self):
        self.url = reverse("v1:role-list")

    def test_when_user_has_no_permission_then_he_gets_an_error(self, client):
        response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            response.data["detail"] == "You do not have permission to perform this action."
        )

    @pytest.mark.parametrize(
        "assign_permission", [{"perm_name": "role_list"}], indirect=True
    )
    def test_when_user_has_permissions_then_he_can_see_roles(
        self, client, assign_permission
    ):
        response = client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("results")[0].get("name") == "Super Admin"
        assert response.data.get("results")[0].get("description") == "Manage the org"
        assert response.data.get("results")[0].get("role_type") == "SYSTEM"
        assert sorted(response.data.get("results")[0].get("users")) == sorted(
            ["John Doe"]
        )
        assert sorted(response.data.get("results")[0].get("permissions")) == sorted(
            ["role_list"]
        )

    @pytest.mark.parametrize(
        "assign_permission", [{"perm_name": "role_create"}], indirect=True
    )
    def test_user_can_create_role(self, client, assign_permission):
        _, user_role, _ = assign_permission
        data = {
            "name": "Manager",
            "organisation": user_role.organisation.id,
            "description": "Manage",
        }
        response = client.post(self.url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get("name") == data["name"]
        assert response.data.get("description") == data["description"]
        assert response.data.get("organisation") == data["organisation"]
        assert response.data.get("permissions") == []
        assert response.data.get("users") == []
