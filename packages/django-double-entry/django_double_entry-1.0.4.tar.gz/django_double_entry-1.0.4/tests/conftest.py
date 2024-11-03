from accounting.models.common import Currency
import pytest
from model_bakery import baker


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def currency():
    return baker.make(Currency, name="Ksh", conversion_rate=1)
