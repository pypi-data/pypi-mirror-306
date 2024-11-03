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
