import pytest
from django.urls import reverse
from rest_framework import status

from pycorpkit.accountx.models.role import Role, RoleTypes

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "assign_permission", [{"perm_name": "role_list"}], indirect=True
)
def test_roles_filters_names_and_types(client, assign_permission):

    assert Role.objects.count() == 1
    filters = {"name": "Super Admin"}
    url = reverse("v1:role-list")
    response = client.get(url, filters)
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("results")[0].get("name") == "Super Admin"
    assert response.data.get("results")[0].get("description") == "Manage the org"
    assert response.data.get("results")[0].get("role_type") == "SYSTEM"
    assert sorted(response.data.get("results")[0].get("users")) == sorted(["John Doe"])
    assert sorted(response.data.get("results")[0].get("permissions")) == sorted(
        ["role_list"]
    )

    filters = {"role_type": RoleTypes.SYSTEM}
    url = reverse("v1:role-list")
    response = client.get(url, filters)
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("results")[0].get("name") == "Super Admin"
    assert response.data.get("results")[0].get("role_type") == "SYSTEM"


@pytest.mark.parametrize(
    "assign_permission", [{"perm_name": "role_list"}], indirect=True
)
def test_roles_filters_non_existent_role_name_and_types(client, assign_permission):

    assert Role.objects.count() == 1
    filters = {"name": "non existent"}
    url = reverse("v1:role-list")
    response = client.get(url, filters)
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("results") == []

    filters = {"role_type": "I dont exist"}
    url = reverse("v1:role-list")
    response = client.get(url, filters)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize(
    "assign_permission", [{"perm_name": "role_list"}], indirect=True
)
def test_roles_filters_names_with_select_box(client, assign_permission):

    _, user_role, _ = assign_permission
    assert Role.objects.count() == 1
    url = reverse("v1:role-list")
    response = client.get(url + "?selectbox=" + str(user_role.role.id))
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("results")[0].get("name") == "Super Admin"
    assert response.data.get("results")[0].get("description") == "Manage the org"
    assert response.data.get("results")[0].get("role_type") == "SYSTEM"
    assert sorted(response.data.get("results")[0].get("users")) == sorted(["John Doe"])
    assert sorted(response.data.get("results")[0].get("permissions")) == sorted(
        ["role_list"]
    )
