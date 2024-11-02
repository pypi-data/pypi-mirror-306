from functools import partial

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
import pytest
from django.db.models.signals import (
    m2m_changed,
    post_delete,
    post_save,
    pre_delete,
    pre_save,
)
from pytest import fixture

from pycorpkit.accountx.permissions.setup import PERM_NODE
from pycorpkit.common.utils.constants import EMAIL, PHONE_NUMBER
from tests.helpers import (
    create_test_branch,
    create_test_contact,
    create_test_department,
    create_test_department_member,
    create_test_organisation,
    create_test_permission,
    create_test_person,
    create_test_role,
    create_test_user,
    create_test_user_profile,
    create_test_user_role,
)


ROLE_VIEW = PERM_NODE("role_list", "View roles")

ROLE_CREATE = PERM_NODE("role_create", "Create roles")

ROLE_EDIT = PERM_NODE("role_edit", "Edit roles")

ROLE_DELETE = PERM_NODE("role_delete", "Delete roles")

ROLE_MANAGE = PERM_NODE(
    "role_manage",
    "Create, Edit and View roles",
    children=(
        ROLE_VIEW,
        ROLE_CREATE,
        ROLE_EDIT,
    ),
)

USER_VIEW = PERM_NODE("user_list", "View users", is_system_level=True)


pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture(autouse=True)
def mute_signals(request):
    """
    This produces the default behaviour to mute all signals.
    By setting autouse=True the fixture is automatically
    invoked and used for each test.
    see: https://www.cameronmaske.com/muting-django-signals-with-a-pytest-fixture/
    """
    # Skip applying, if marked with `@pytest.mark.enable_signals`
    if "enable_signals" in request.keywords:
        return

    signals = [pre_save, post_save, pre_delete, post_delete, m2m_changed]
    restore = {}
    for signal in signals:
        # Temporally remove the signal's receivers (a.k.a attached functions)
        restore[signal] = signal.receivers
        signal.receivers = []

    def restore_signals():
        # When the test tears down, restore the signals.
        for signal, receivers in restore.items():
            signal.receivers = receivers

    # Called after a test has finished.
    request.addfinalizer(restore_signals)


@pytest.fixture
def organisation():
    return create_test_organisation()


@pytest.fixture
def user():
    return create_test_user()


@pytest.fixture
def person():
    return create_test_person()


@pytest.fixture
def contact(person):
    create_test_contact(person, PHONE_NUMBER, "0700100200", True)
    create_test_contact(person, EMAIL, "mail@mail.com", True)


@pytest.fixture
def branch(organisation):
    return create_test_branch("Main Branch", organisation)


@pytest.fixture
def department(organisation):
    return create_test_department("Main Department", organisation)


@pytest.fixture
def role(organisation):
    return create_test_role("Super Admin", organisation)


@pytest.fixture
def user_profile(person, user):
    """This profile is not tied to any organisation."""
    return create_test_user_profile(user, person)


@pytest.fixture
def user_role(role, user_profile):
    """Adds the provided user_profile to the provided role."""
    perms = [ROLE_CREATE.name, ROLE_VIEW.name, ROLE_EDIT.name]
    for perm in perms:
        create_test_permission(perm, role)
    create_test_user_role(role=role, user_profile=user_profile)


@pytest.fixture
def profile_in_org(department, user_profile, user_role):
    """Adds the provided user_profile to the departments organisation."""
    create_test_department_member(user_profile, department)
    return user_profile, department


@pytest.fixture
def assign_permission(role, user_profile, department, request):
    """Used to assign a user a permission in the default departments organisation."""
    perm_name = request.param.get("perm_name", USER_VIEW.name)
    department_member = create_test_department_member(user_profile, department)
    perm = create_test_permission(perm_name, role)
    user_role = create_test_user_role(role=role, user_profile=user_profile)
    return perm, user_role, department_member


@fixture
def unauthenticated_client():
    """Use this for APIs that don't require an authentication."""
    client = APIClient()
    return client


@fixture
def client_without_org(user, contact):
    """Use this for APIs that don't need to provide the ORG header."""
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
    return client


@pytest.fixture
def client(user, contact, organisation):
    """Use this for all APIs that require an ORG header and an authentication."""
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    current_org_headers = {
        "HTTP_ORGANISATION_ID": str(organisation.id),
    }
    client = APIClient()
    client.get = partial(client.get, **current_org_headers)
    client.patch = partial(client.patch, **current_org_headers)
    client.post = partial(client.post, **current_org_headers)
    client.delete = partial(client.delete, **current_org_headers)
    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
    return client
