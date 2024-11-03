Core Components
--------------

Account Headings
~~~~~~~~~~~~~~~
.. class:: AccountHeading

A classification system for accounts that defines their type and behavior.

**Fields:**

- ``heading`` (CharField): The name of the heading
- ``heading_type`` (CharField): Type of the account (choices defined in ACCOUNT_TYPE)
- ``balance_type`` (CharField): Balance type, either "dr" (Debit) or "cr" (Credit)
- ``number`` (IntegerField): Heading number for ordering/reference
- ``tracker`` (IntegerField): Tracks changes/versions of the heading

Accounts
~~~~~~~~
.. class:: Account

Represents individual accounts in the accounting system. Supports hierarchical structure with parent-child relationships.

**Fields:**

- ``name`` (CharField): Account name
- ``is_control_account`` (BooleanField): Indicates if this is a control account
- ``is_active`` (BooleanField): Account status
- ``heading`` (ForeignKey): Reference to AccountHeading
- ``number`` (CharField): Account number/code
- ``parent`` (ForeignKey): Reference to parent account (self-referential)

**Key Methods:**

.. method:: period_records(end, extra_filters=None)

   Retrieves accounting entries for a specific period.

   :param end: End date for the period
   :param extra_filters: Additional filtering criteria
   :return: QuerySet of accounting entries

.. method:: period_total(field, end, extra_filters=None)

   Calculates total value of entries up to specified end date.

   :param field: Field to total ('dr_amount' or 'cr_amount')
   :param end: End date for calculation
   :param extra_filters: Additional filtering criteria
   :return: Decimal total value

.. method:: balance(end=None, extra_filters=None, dr_filters=None, cr_filters=None)

   Calculates account balance at a given date.

   :param end: End date for balance calculation
   :param extra_filters: General filtering criteria
   :param dr_filters: Filters specific to debit entries
   :param cr_filters: Filters specific to credit entries
   :return: Decimal balance value

Accounting Transactions
~~~~~~~~~~~~~~~~~~~~~
.. class:: AccountingTransaction

Represents a complete double-entry transaction with balanced debit and credit entries.

**Fields:**

- ``description`` (TextField): Transaction description
- ``dr_entry`` (AccountingEntry): Debit entry
- ``cr_entry`` (AccountingEntry): Credit entry

**Key Methods:**

.. method:: validate_entries_value()

   Ensures that transaction entries balance according to double-entry principles.

.. method:: save(*args, **kwargs)

   Saves transaction and associated entries atomically.

Accounting Entries
~~~~~~~~~~~~~~~~
.. class:: AccountingEntry

Individual ledger entries that make up transactions.

**Fields:**

- ``account`` (ForeignKey): Reference to Account
- ``transaction`` (ForeignKey): Reference to AccountingTransaction
- ``dr_amount`` (DecimalField): Debit amount
- ``cr_amount`` (DecimalField): Credit amount
- ``entry_date`` (DateTimeField): Date of entry
- ``currency`` (ForeignKey): Reference to Currency
- ``description`` (CharField): Entry description

**Properties:**

.. property:: dr_value

   Calculated debit value in default currency

.. property:: cr_value

   Calculated credit value in default currency

.. property:: amount

   Total amount in default currency

Usage Example
------------

.. code-block:: python

    # Create a transaction with balanced entries
    transaction = AccountingTransaction(
        description="Monthly rent payment",
        dr_entry=AccountingEntry(
            account=rent_expense_account,
            dr_amount=1000.00,
            currency=usd_currency
        ),
        cr_entry=AccountingEntry(
            account=bank_account,
            cr_amount=1000.00,
            currency=usd_currency
        )
    )
    transaction.save()  # This will save both the transaction and its entries

Important Notes
-------------

1. All transactions must follow double-entry principles (debits must equal credits)
2. Entries must be either debit OR credit, not both
3. All monetary values are stored with 4 decimal places
4. Currency conversion is handled automatically based on currency conversion rates
5. Control accounts aggregate entries from their child accounts
