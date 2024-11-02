import importlib
from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def check_permissions_path():
    permissions_path = getattr(settings, "PERMISSIONS_PATH")
    if not permissions_path:
        raise ImproperlyConfigured("variable `PERMISSIONS_PATH` must be configured.")

    default_roles = getattr(settings, "DEFAULT_ROLES")
    if not default_roles:
        raise ImproperlyConfigured(
            "variable `DEFAULT_ROLES` must be configured."
        )

    permissions_path_module = importlib.import_module(permissions_path)
    return permissions_path_module, default_roles


def check_jwt_settings():
    simple_jwt = getattr(settings, "SIMPLE_JWT", None)
    if simple_jwt is None:
        raise ImproperlyConfigured(
            "SIMPLE_JWT setting is required but not set in your settings file."
        )

    if not isinstance(simple_jwt, dict):
        raise ImproperlyConfigured("SIMPLE_JWT must be a dictionary.")

    required_fields = ["ACCESS_TOKEN_LIFETIME", "REFRESH_TOKEN_LIFETIME"]

    for field in required_fields:
        if field not in simple_jwt:
            raise ImproperlyConfigured(
                f"SIMPLE_JWT['{field}'] is required but not set in your settings file."
            )

        if not isinstance(simple_jwt[field], timedelta):
            raise ImproperlyConfigured(
                f"SIMPLE_JWT['{field}'] must be a timedelta object."
            )
    return simple_jwt


def get_client_settings():
    """
    Validates and returns required client settings.
    Raises ImproperlyConfigured if any required settings are missing.

    Returns:
        dict: Dictionary containing the validated settings
    """
    required_settings = {
        "AUTH_USER_MODEL": None,
        "DEFAULT_FROM_EMAIL": None,
        "APP_NAME": None,
        "CLIENT_DOMAIN": None,
    }

    for setting_name in required_settings:
        if not hasattr(settings, setting_name):
            raise ImproperlyConfigured(
                f"{setting_name} is required but not set in your settings file."
            )

    config = {
        setting_name: getattr(settings, setting_name)
        for setting_name in required_settings
    }

    if "." not in config["AUTH_USER_MODEL"]:
        raise ImproperlyConfigured(
            "AUTH_USER_MODEL must be of the form 'app_label.ModelName'"
        )

    if "@" not in config["DEFAULT_FROM_EMAIL"]:
        raise ImproperlyConfigured("DEFAULT_FROM_EMAIL must be a valid email address")

    if not config["CLIENT_DOMAIN"].startswith(("http://", "https://")):
        raise ImproperlyConfigured(
            "CLIENT_DOMAIN must start with 'http://' or 'https://'"
        )

    if not config["APP_NAME"]:
        raise ImproperlyConfigured("APP_NAME cannot be empty")

    return config


def compile_settings():
    """Compiles and validates all package settings and defaults.

    Provides basic checks to ensure required settings are declared
    and applies defaults for all missing settings.

    Returns:
        dict: All possible pycorpkit settings.
    """
    user_reset_password_text = getattr(
        settings, "USER_RESET_PASSWORD_TEXT_PATH", "email/user_reset_password.txt"
    )
    user_reset_password_html = getattr(
        settings, "USER_RESET_PASSWORD_HTML_PATH", "email/user_reset_password.html"
    )

    verification_code_length = getattr(settings, "VERIFICATION_CODE_LENGTH", 6)
    verification_code_chars = getattr(settings, "VERIFICATION_CODE_CHARS", "123456789")
    verification_code_days_expiry = getattr(
        settings, "VERIFICATION_CODE_DAYS_EXPIRY", 3
    )

    invite_code_days_expire = getattr(settings, "INVITE_CODE_DAYS_EXPIRY", 7)
    secret_key = getattr(settings, "SECRET_KEY", "secret_keys")

    user_invite_text = getattr(
        settings, "USER_INVITE_TEXT_PATH", "email/user_invite.txt"
    )
    user_invite_html = getattr(
        settings, "USER_INVITE_HTML_PATH", "email/user_invite.html"
    )

    user_activate_text = getattr(
        settings, "USER_ACTIVATE_TEXT_PATH", "email/signup_confirm.txt"
    )
    user_activate_html = getattr(
        settings, "USER_ACTIVATE_HTML_PATH", "email/signup_confirm.html"
    )

    org_signup_text = getattr(
        settings, "ORG_SIGNUP_TEXT_PATH", "email/org_signup_confirm.txt"
    )
    org_signup_html = getattr(
        settings, "ORG_SIGNUP_HTML_PATH", "email/org_signup_confirm.html"
    )
    perms_path, default_roles = check_permissions_path()
    simple_jwt = check_jwt_settings()
    settings_config = get_client_settings()

    return {
        "APP_NAME": settings_config["APP_NAME"],
        "USER_RESET_PASSWORD_TEXT_PATH": user_reset_password_text,
        "USER_RESET_PASSWORD_HTML_PATH": user_reset_password_html,
        "USER_INVITE_TEXT_PATH": user_invite_text,
        "USER_INVITE_HTML_PATH": user_invite_html,
        "USER_ACTIVATE_TEXT_PATH": user_activate_text,
        "USER_ACTIVATE_HTML_PATH": user_activate_html,
        "ORG_SIGNUP_TEXT_PATH": org_signup_text,
        "ORG_SIGNUP_HTML_PATH": org_signup_html,
        "VERIFICATION_CODE_LENGTH": verification_code_length,
        "VERIFICATION_CODE_CHARS": verification_code_chars,
        "VERIFICATION_CODE_DAYS_EXPIRY": verification_code_days_expiry,
        "SIMPLE_JWT": simple_jwt,
        "INVITE_CODE_DAYS_EXPIRY": invite_code_days_expire,
        "SECRET_KEY": secret_key,
        "CLIENT_DOMAIN": settings_config["CLIENT_DOMAIN"],
        "AUTH_USER_MODEL": settings_config["AUTH_USER_MODEL"],
        "DEFAULT_FROM_EMAIL": settings_config["DEFAULT_FROM_EMAIL"],
        "PERMISSIONS_PATH": perms_path,
        "DEFAULT_ROLES": default_roles,
    }


SETTINGS = compile_settings()
