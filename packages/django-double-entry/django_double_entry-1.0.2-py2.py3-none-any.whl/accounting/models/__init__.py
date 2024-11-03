from decimal import Decimal
import uuid

from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils import timezone

from accounting.models.common import ACCOUNT_TYPE, Base, Currency


BALANCE_TYPES = (("dr", "DR"), ("cr", "CR"))


class AccountHeading(Base):
    """
    A classification system for accounts that defines their type and behavior.
    """

    heading = models.CharField(max_length=255)
    heading_type = models.CharField(max_length=255, choices=ACCOUNT_TYPE)
    balance_type = models.CharField(max_length=255, choices=BALANCE_TYPES)
    number = models.IntegerField()
    tracker = models.IntegerField(default=0)
    system_id = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.heading


class Account(Base):
    """_summary_
    Represents individual accounts in the accounting system.
    Supports hierarchical structure with parent-child relationships.
    """

    name = models.CharField(max_length=100)
    is_control_account = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    heading = models.ForeignKey(
        AccountHeading, related_name="child_accounts", on_delete=models.PROTECT
    )
    number = models.CharField(max_length=255, blank=True)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="children",
        db_index=True,
    )
    system_id = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return "{} - {}".format(self.number, self.name)

    @property
    def account_name(self):
        return "{} - {}".format(self.number, self.name)

    def period_records(self, end, extra_filters=None):
        """Get period accounting entries."""
        new_end = end or timezone.now()
        filters = {"created__lte": new_end}
        if extra_filters:
            assert isinstance(
                extra_filters, dict
            ), "Extra filters should be a dictionary."
            filters.update(extra_filters)

        if self.is_control_account:
            account_entries = AccountingEntry.objects.filter(account__parent=self)
        else:
            account_entries = self.account_entries
        return account_entries.filter(**filters)

    def period_total(self, field, end, extra_filters=None):
        """Get the total value of entries to the end date specified."""
        entries = self.period_records(end, extra_filters)
        field_value = models.F(field) * models.F("currency__conversion_rate")
        entries = entries.annotate(field_value=field_value)
        return entries.aggregate(value_sum=models.Sum("field_value"))[
            "value_sum"
        ] or Decimal("0")

    def dr_total(self, end=None, extra_filters=None):
        """Calculate the total of debit entries for the period so far."""
        return self.period_total("dr_amount", end, extra_filters)

    def cr_total(self, end=None, extra_filters=None):
        """Calculate the total of credit entries for the period so far."""
        return self.period_total("cr_amount", end, extra_filters)

    def balance(self, end=None, extra_filters=None, dr_filters=None, cr_filters=None):
        """Get the balance of an account at a given date within a year."""
        if dr_filters:
            dr_filters.update(extra_filters)

        if cr_filters:
            cr_filters.update(extra_filters)

        dr_filters = dr_filters or extra_filters
        cr_filters = cr_filters or extra_filters

        cr_total = self.cr_total(end, cr_filters)
        dr_total = self.dr_total(end, dr_filters)
        if self.balance_type == "cr":
            return cr_total - dr_total
        else:
            return dr_total - cr_total

    @property
    def balance_type(self):
        return self.heading.balance_type

    @property
    def current_balance(self):
        return self.balance()

    class Meta:
        ordering = ("-updated", "-created")


class AccountingTransaction(Base):
    """
    Represents a complete double-entry transaction with balanced debit and credit entries.
    """

    def __init__(self, *args, **kwargs):
        """Initialize a transaction with a debit and credit entry."""
        self.dr_entry = kwargs.pop("dr_entry", None)
        self.cr_entry = kwargs.pop("cr_entry", None)

        super().__init__(*args, **kwargs)

    description = models.TextField()

    dr_entry = None
    cr_entry = None

    def validate_dr_entry(self):
        """Ensure that every transaction has a debit entry."""
        if not self.dr_entry:
            raise ValidationError({"dr_entry": "The debit entry is required."})

    def validate_cr_entry(self):
        """Ensure that every transaction has a credit entry."""
        if not self.cr_entry:
            raise ValidationError({"cr_entry": "The credit entry is required."})

    def validate_entries_value(self):
        """Ensure that transaction entries balance."""
        entries_set = self.dr_entry and self.cr_entry
        if entries_set and (self.dr_entry.amount != self.cr_entry.amount):
            raise ValidationError(
                "Transaction does not observe double entry. "
                "{} (dr) - {} != {} (cr) - {}".format(
                    self.dr_entry.account.name,
                    round(self.dr_entry.amount, 2),
                    self.cr_entry.account.name,
                    round(self.cr_entry.amount, 2),
                )
            )

    def clean(self, *args, **kwargs):
        self.validate_cr_entry()
        self.validate_dr_entry()
        self.validate_entries_value()
        super().clean(*args, **kwargs)

    @transaction.atomic
    def save(self, *args, **kwargs):
        """Save a transaction AND it's accompanying entries."""
        self.full_clean()  # Ensure validation is checked before saving
        super().save(*args, **kwargs)
        self.dr_entry.transaction = self
        self.cr_entry.transaction = self

        self.dr_entry.save()
        self.cr_entry.save()


class AccountingEntry(Base):
    """_summary_
    Individual ledger entries that make up transactions.
    """

    account = models.ForeignKey(
        Account,
        related_name="account_entries",
        null=False,
        blank=False,
        on_delete=models.deletion.PROTECT,
    )
    transaction = models.ForeignKey(
        AccountingTransaction,
        related_name="transaction_account_entries",
        on_delete=models.PROTECT,
    )
    dr_amount = models.DecimalField(max_digits=16, decimal_places=4, default=0)
    cr_amount = models.DecimalField(max_digits=16, decimal_places=4, default=0)
    entry_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    currency = models.ForeignKey(
        Currency, related_name="currency", on_delete=models.deletion.PROTECT
    )
    description = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.account.name} {self.currency.name} {self.amount}"

    def validate_amount(self):
        """Ensure that an account entry is either a debit or credit amount."""
        if self.dr_amount and self.cr_amount:
            raise ValidationError(
                "An account entry can only be a dr entry or a cr entry "
                "at any given time. Kindly provide either of dr_amount or "
                "cr_amount and not both of them"
            )

    @property
    def dr_value(self):
        """Calculate the debit value in the default currency."""
        return (self.dr_amount * self.currency.conversion_rate) or 0

    @property
    def cr_value(self):
        """Calculate the credit value in the default currency."""
        return (self.cr_amount * self.currency.conversion_rate) or 0

    @property
    def amount(self):
        """Calculate the amount in the default currency."""
        amount = self.dr_amount or self.cr_amount
        return amount * self.currency.conversion_rate

    def clean(self, *args, **kwargs):
        self.validate_amount()
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
