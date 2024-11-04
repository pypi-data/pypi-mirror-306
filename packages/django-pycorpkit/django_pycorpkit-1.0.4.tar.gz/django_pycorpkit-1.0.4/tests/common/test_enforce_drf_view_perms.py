import pytest
from django.core.exceptions import ImproperlyConfigured

from pycorpkit.accountx.permissions.enforce import EnforceDRFViewPermission
from pycorpkit.accountx.permissions.setup import PERM_NODE


ORGANISATION_VIEW = PERM_NODE(
    "organisation_list",
    "View organisations",
    is_deprecated=False,
    is_system_level=True,
)
ORGANISATION_EDIT = PERM_NODE(
    "organisation_edit",
    "Edit organisations",
    is_deprecated=False,
    is_system_level=True,
)


@pytest.fixture
def drf_perm():
    return EnforceDRFViewPermission()


def test_get_method_perms_retrives_permissions_based_on_http(drf_perm):
    perm_dict = {}
    assert drf_perm._get_method_perms("GET", perm_dict) == []

    perm_dict = {
        "GET": [
            ORGANISATION_EDIT.name,
        ]
    }
    assert drf_perm._get_method_perms("GET", perm_dict) == [
        ORGANISATION_EDIT.name,
    ]

    perm_dict = {
        "GET": [
            ORGANISATION_EDIT.name,
        ]
    }
    assert drf_perm._get_method_perms("HEAD", perm_dict) == [
        ORGANISATION_EDIT.name,
    ]
    assert drf_perm._get_method_perms("OPTIONS", perm_dict) == [
        ORGANISATION_EDIT.name,
    ]

    perm_dict = {
        "PATCH": [
            ORGANISATION_EDIT.name,
        ]
    }
    assert drf_perm._get_method_perms("PUT", perm_dict) == [
        ORGANISATION_EDIT.name,
    ]

    perm_dict = {
        "PATCH": [
            ORGANISATION_EDIT.name,
        ],
        "PUT": [
            ORGANISATION_VIEW.name,
        ],
    }
    assert drf_perm._get_method_perms("PUT", perm_dict) == [
        ORGANISATION_VIEW.name,
    ]

    perm_dict = {"GET": "pop"}
    with pytest.raises(ImproperlyConfigured) as ex:
        drf_perm._get_method_perms("GET", perm_dict)
    assert str(ex.value) == "HTTP `method` permissions should be a list"


def test_encforce_drf_flatten_perm_list(drf_perm):
    fpl = drf_perm._flatten_perm_list
    assert fpl(None) == []
    assert fpl([]) == []
    assert fpl(
        [
            (
                "a",
                "A",
            )
        ]
    ) == ["a"]
    assert fpl(
        [
            (
                "a",
                "A",
            ),
            ("b", "B"),
        ]
    ) == ["a", "b"]
    assert fpl(
        [
            (
                "a",
                "A",
            ),
            ("b", "B"),
            [
                (
                    "c",
                    "C",
                ),
                ("d", "D"),
            ],
        ]
    ) == ["a", "b", "c", "d"]

    with pytest.raises(ImproperlyConfigured) as ex:
        fpl(["a"])
    assert str(ex.value) == ("Permissions should be either a tuple or a list")
    with pytest.raises(ImproperlyConfigured) as ex:
        assert fpl(
            [
                [
                    (
                        "a",
                        "A",
                    ),
                    "b",
                ]
            ]
        )
    assert str(ex.value) == ("Permissions should be either a tuple or a list")


@pytest.mark.django_db
def test_enforce_drf_permissions_has_permissions(drf_perm, user, organisation):
    view = type("_V", (object,), {})()
    request = type(
        "_R",
        (object,),
        {"method": "GET", "user": user, "organisation_id": organisation.id},
    )()
    assert drf_perm.has_permission(request, view)

    view = type("_V", (object,), {"permissions": ("llll",)})()
    with pytest.raises(ImproperlyConfigured) as ex:
        drf_perm.has_permission(request, view)
    assert str(ex.value) == "Permissions should be a dict."

    view = type("_V", (object,), {"permissions": {"GET": []}})()
    assert drf_perm.has_permission(request, view)

    view = type("_V", (object,), {"permissions": {"GET": [("a", "A")]}})()
    assert not drf_perm.has_permission(request, view)
