Quick start
===========

.. _installation:

1. Install package

.. code-block:: python

   pip install django-double-entry


2. Add "django-double-entry" to your ``INSTALLED_APPS`` setting:

   .. code-block:: python

      INSTALLED_APPS = [
          ...
          'accounting',
      ]

3. Run migrations:

   .. code-block:: python

      python manage.py migrate
