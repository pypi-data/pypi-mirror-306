import logging
from collections import defaultdict
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from pycorpkit.common.utils.conf import SETTINGS

LOGGER = logging.getLogger(__name__)


class InvalidVerificationCodeError(Exception):
    pass


class ExpiredVerificationCodeError(Exception):
    pass


def flatten(to_flatten, flat_list):
    for i in to_flatten:
        if isinstance(i, list) or isinstance(i, tuple):
            flatten(i, flat_list)
        else:
            if i is not None:
                flat_list.append(i)
    return flat_list


class CustomUserManager(BaseUserManager):

    def change_password(self, user, current_password, password):
        user = self.get(id=user.id)
        if not user.check_password(current_password):
            return None

        user.set_password(password)
        user.save()
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        user = self.create_user(email=email, password=password, **extra_fields)
        user.is_admin = True
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def generate_verify_code(self, email):
        """
        Generates a new verification code returns user
        """
        try:
            user = self.get(email__iexact=email)
        except get_user_model().DoesNotExist:
            raise InvalidVerificationCodeError(
                "We can't find that email address, sorry!"
            )
        user.verify_code = get_random_string(
            length=SETTINGS["VERIFICATION_CODE_LENGTH"],
            allowed_chars=SETTINGS["VERIFICATION_CODE_CHARS"],
        )
        user.verify_code_expire = timezone.now() + timedelta(
            days=SETTINGS["VERIFICATION_CODE_DAYS_EXPIRY"]
        )
        user.save()
        return user

    def make_user_active(self, email, verify_code):
        """Activate user and ensure verification code is not used again."""
        try:
            user = self.get(email=email)
        except get_user_model().DoesNotExist:
            raise InvalidVerificationCodeError("User does not exist.")

        if not user.verify_code or user.verify_code != verify_code:
            raise InvalidVerificationCodeError("Verification code is invalid.")

        if user.verify_code_expire < timezone.now():
            raise ExpiredVerificationCodeError("Verification code is expired.")

        user.verify_code = None
        user.verify_code_expire = None
        user.is_verified = True
        user.is_active = True
        user.save()


class User(AbstractUser):
    """
    This represents a logged in user into the system.
    """

    email = models.EmailField(_("email address"), unique=True, db_index=True)
    is_suspended = models.BooleanField(default=False)
    agreed_to_terms = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    verify_code = models.CharField(
        max_length=512,
        blank=True,
        null=True,
        help_text="User account verification code.",
        editable=False,
    )
    verify_code_expire = models.DateTimeField(
        max_length=512,
        blank=True,
        null=True,
        help_text="Verification  code expire date.",
        editable=False,
    )
    is_verified = models.BooleanField(default=False)
    change_pass_at_next_login = models.BooleanField(
        "Change password at next login", default=False
    )
    is_system_user = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        indexes = [
            models.Index(fields=['email'], name='user_email_idx'),
        ]

    def __str__(self):
        return self.email

    @property
    def profiles(self):
        return self.user_profile.all()

    @property
    def person(self):
        """
        User MUST have only one person record,
        here we return the default that was created on signup
        if the user has not created a profile yet.
        """
        for profile in self.profiles:
            if profile.person:
                return profile.person

        return self.default_contact.person

    @property
    def contacts(self):
        """
        Returns all usercontacts, if they don't have a profile
        setup, return the default that was created on signup.
        """
        from pycorpkit.common.models.person import PersonContact

        all_contacts = set(
            contact
            for profile in self.profiles.all()
            for contact in profile.person.person_contacts.all()
        )
        if not all_contacts:
            return PersonContact.objects.filter(person=self.person).all()
        return list(all_contacts)

    @property
    def default_contact(self):
        """
        Returns default contact created on signup.
        """
        from pycorpkit.common.models.person import PersonContact

        return PersonContact.objects.get(contact_value=self.email)

    @property
    def departments(self):
        """
        Collect department memberships across all profiles
        """
        from pycorpkit.org_structure.models.department import Department

        user_departments = Department.objects.filter(
            department_users__user__in=self.profiles
        ).distinct()

        return user_departments

    @property
    def permission_names(self):
        return self.get_all_grouped_permissions()

    @property
    def role_names(self):
        """Groups a users roles per organisation."""
        org_roles = defaultdict(list)
        for profile in self.profiles:
            user_roles = profile.user_roles.values_list("role__name", flat=True)
            department_member = profile.user_department.first()
            if department_member:
                organisation_id = department_member.department.organisation.id
                org_roles[organisation_id].extend(user_roles)

        for org_id, roles in org_roles.items():
            org_roles[org_id] = list(set(roles))
        return dict(org_roles)

    def has_permissions(self, permissions, organisation_id):
        """Check if user has the specified permissions in the given organisation."""
        if not organisation_id:
            return []

        return set(permissions).intersection(
            set(self.get_user_permissions(organisation_id))
        ) == set(permissions)

    def get_user_permissions(self, organisation_id):
        """
        Get permissions assigned to this user in the given organisation.
        """
        from pycorpkit.accountx.models.role import RolePermission, UserRole

        user_roles = UserRole.objects.filter(
            user_profile__in=self.profiles, organisation_id=organisation_id
        )
        role_permissions = RolePermission.objects.filter(
            role__in=[user_role.role for user_role in user_roles],
            organisation_id=organisation_id,
        ).distinct()

        all_permissions = []
        for rp in role_permissions:
            all_permissions.append(rp.permission.name)
            if rp.permission.children:
                all_permissions.extend(rp.permission.children)
        return all_permissions

    def get_all_grouped_permissions(self):
        """
        Get all permissions assigned to this user in all the organisations
        he is a member of..
        """
        from pycorpkit.accountx.models.role import RolePermission, UserRole

        org_permissions = defaultdict(set)
        for department in self.departments:
            organisation_id = department.organisation.id
            user_roles = UserRole.objects.filter(
                user_profile__in=self.profiles,
                organisation_id=department.organisation.id,
            )
            role_permissions = RolePermission.objects.filter(
                role__in=user_roles.values_list("role", flat=True),
                organisation_id=department.organisation.id,
            ).distinct()

            for rp in role_permissions:
                permission_name = rp.permission.name
                org_permissions[organisation_id].add(permission_name)

                if rp.permission.children:
                    for child in rp.permission.children:
                        org_permissions[organisation_id].add(child)
        return {
            org_id: list(permissions) for org_id, permissions in org_permissions.items()
        }
