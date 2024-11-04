About
-----
A Django-based double-entry bookkeeping system that provides a robust framework for handling financial transactions.

Inspired by martinfowler accounting patterns

https://www.martinfowler.com/eaaDev/AccountingNarrative.html


Features
--------
+ All transactions must follow double-entry principles (debits must equal credits)
+ Entries must be either debit OR credit, not both
+ All monetary values are stored with 4 decimal places
+ Currency conversion is handled automatically based on currency conversion rates
+ Control accounts aggregate entries from their child accounts

Installation
------------

1. Install package

.. code-block:: python

   pip install django-double-entry


2. Add "accounting" to your ``INSTALLED_APPS`` setting:

   .. code-block:: python

      INSTALLED_APPS = [
          ...
          'accounting',
      ]

3. Run migrations:

   .. code-block:: python

      python manage.py migrate


Documentation
-------------

https://django-double-entry.readthedocs.io/en/latest/index.html
