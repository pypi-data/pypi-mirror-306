About
=====
A reusable DRF library that provides reusable components.

Installation
============
.. code-block:: bash

    pip install django-pycorpkit

Quick start
===========
1. Add "django-pycorpkit" to your INSTALLED_APPS setting:

   .. code-block:: python

       INSTALLED_APPS = [
           ...
           "pycorpkit.common",
           "pycorpkit.accountx",
           "pycorpkit.org_structure",
       ]

2. Include the django_sample_lib URLconf in your project urls.py:

   .. code-block:: python

       path('api/', include('pycorpkit.urls')),

3. Run migrations:

   .. code-block:: bash

       python manage.py migrate

4. Add exception handler and default backend filter:

   .. code-block:: python

       REST_FRAMEWORK = {
           "EXCEPTION_HANDLER": "pycorpkit.common.utils.exception_handler.custom_exception_handler",
           "DEFAULT_PERMISSION_CLASSES": [
               "pycorpkit.accountx.permissions.enforce.EnforceDRFViewPermission",
           ],
           "DEFAULT_FILTER_BACKENDS": (
               "pycorpkit.common.filters.base.OrganisationFilterBackend",
           ),
       }

5. Add required variables in settings file:

   .. code-block:: python

       PERMISSIONS_PATH = "testapp.perms"
       APP_NAME = "PyCorpKit"
       CLIENT_DOMAIN = "http://domain.com/"
       AUTH_USER_MODEL = "accountx.User"
       DEFAULT_FROM_EMAIL = "admin@example.com"
       SIMPLE_JWT = {
           "ACCESS_TOKEN_LIFETIME": timedelta(seconds=3600),
           "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
       }

6. INCLUDE `django_rest_passwordreset` in installed apps

    .. code-block:: python

        INSTALLED_APPS = (
            'django_rest_passwordreset',
        )

7. Add `PhoneModelBackend` to `AUTHENTICATION_BACKENDS`

    .. code-block:: python
    
        AUTHENTICATION_BACKENDS = [
            'django.contrib.auth.backends.ModelBackend',
            # add the below after `ModelBackend`
            'pycorpkit.common.utils.phone_backend.PhoneModelBackend',
        ]

8. Add organisation `middleware`

    .. code-block:: python 

        MIDDLEWARE = [
            "pycorpkit.common.utils.middleware.OrganisationIDMiddleware",
        ]

9. Define `DEFAULT_ROLES` in settings

    .. code-block:: python
        
        DEFAULT_ROLES = {
            "Organisation Admin": ORGANISATION_ADMIN,
            "Branch Admin": BRANCH_ADMIN,
            "Department Admin": DEPARTMENT_ADMIN,
            "User": PROFILE_ADMIN,
        }

Development
===========
To set up the development environment:

1. Clone the repository
2. Create a virtual environment and activate it
3. Install development dependencies:

   .. code-block:: bash

       pip install -e ".[dev]"

4. Run tests:

   .. code-block:: bash

       python -m pytest tests
       # OR
       pytest tests/

Install test dependencies
=========================
.. code-block:: bash

    pip install -e ".[test]"

Making migrations
=================
.. code-block:: bash

    python testapp/manage.py makemigrations
    python testapp/manage.py makemigrations <app_name> --empty

Migrate
=======
.. code-block:: bash

    python testapp/manage.py migrate