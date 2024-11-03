import uuid

from django.db import models
from django.utils import timezone
from dateutil import parser


class Base(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(null=True, blank=True)
    updated = models.DateTimeField(default=timezone.now)
    updated_by = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ("-updated", "-created")


class Currency(Base):
    name = models.CharField(max_length=50, null=False, unique=True)
    code = models.CharField(max_length=5, null=False, unique=True)
    is_default = models.BooleanField(default=False)
    conversion_rate = models.DecimalField(
        max_digits=15, decimal_places=4, null=True, blank=True
    )
    system_id = models.UUIDField(default=uuid.uuid4, editable=False)


ACCOUNT_TYPE = (
    ("asset", "Asset"),
    ("liability", "Liability"),
    ("revenue", "Revenue"),
    ("expense", "Expense"),
    ("equity", "Equity"),
)


def string_date_to_datetime(date_to_format):
    """Format string dates into datetime objects.

    ``parser.parse`` is timezone aware unlike ``datetime.strptime``

    Outputs for both scenarios:
        1. parser.parse('2016-10-10T10:34:23.434543Z')
        >>> datetime.datetime(
                        2016, 10, 10, 10, 34, 23, 434543, tzinfo=tzutc())

        2. datetime.strptime('2016-10-10T10:34:23.434543Z',
                             '%Y-%m-%dT%H:%M:%S.%fZ')
        >>> datetime.datetime(2016, 8, 24, 20, 6, 20, 403726)

    In cases where we need to do date addition or subtraction, we cannot
    do the math when one value is timezone aware while the other is
    timezone naive.
    """
    return parser.parse(date_to_format) if date_to_format else None


DEFAULT_ACCOUNT_HEADINGS = [
    {
        "balance_type": "dr",
        "heading": "Current Assets",
        "heading_type": "asset",
        "number": 2000,
        "tracker": 18,
        "system_id": "1a6688b1-e6b8-407b-bcb4-2103400167b0",
    },
    {
        "balance_type": "cr",
        "heading": "Current Liabilities",
        "heading_type": "liability",
        "number": 3000,
        "tracker": 6,
        "system_id": "bf6dd49b-6759-48a4-88c8-198dec898a21",
    },
    {
        "balance_type": "cr",
        "heading": "Sales",
        "heading_type": "revenue",
        "number": 5,
        "tracker": 5,
        "system_id": "42328099-c91c-4666-a0e8-8fb5c3ac1c03",
    },
    {
        "balance_type": "dr",
        "heading": "Tax",
        "heading_type": "expense",
        "number": 4000,
        "tracker": 0,
        "system_id": "907b0d27-0d38-4cac-9d64-2d114e58c308",
    },
]


DEFAULT_ACCOUNTS = [
    {
        "name": "Account Receivables Control",
        "is_control_account": True,
        "system_id": "b7c33157-3a65-41e6-a08c-565b672a5baf",
        "heading": {"system_id": "1a6688b1-e6b8-407b-bcb4-2103400167b0"},
    },
    {
        "name": "Account Payables Control",
        "is_control_account": True,
        "system_id": "2d8051b3-075d-4726-9ac8-20d5cb783b82",
        "heading": {"system_id": "bf6dd49b-6759-48a4-88c8-198dec898a21"},
    },
    {
        "name": "Cash/Bank",
        "is_control_account": False,
        "system_id": "b39c5ec9-0140-49f0-b081-ceb76faccba8",
        "heading": {"system_id": "1a6688b1-e6b8-407b-bcb4-2103400167b0"},
    },
]
