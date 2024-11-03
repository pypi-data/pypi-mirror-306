from accounting.models.common import Currency
import pytest
from django.core.exceptions import ValidationError
from model_bakery import baker
from model_bakery.recipe import Recipe

from accounting.models import Account, AccountingTransaction, AccountingEntry


class TestAccountTransaction:
    def test_transaction(self, currency):
        """Test double entry in transaction model."""
        account = baker.make(Account, name="Cash")
        cr_account = baker.make(Account, name="Bank")
        entry_recipe = Recipe(
            AccountingEntry,
            currency=currency,
        )

        dr_entry = entry_recipe.prepare(dr_amount=10000, account=account)
        cr_entry = entry_recipe.prepare(cr_amount=10000, account=cr_account)

        with pytest.raises(ValidationError) as e:
            baker.make(
                AccountingTransaction,
                cr_entry=cr_entry,
            )
            assert "The debit entry is required." in e.value.messages

        with pytest.raises(ValidationError) as e:
            baker.make(
                AccountingTransaction,
                dr_entry=cr_entry,
            )
            assert "The credit entry is required." in e.value.messages

        t = baker.make(
            AccountingTransaction,
            dr_entry=dr_entry,
            cr_entry=cr_entry,
        )
        assert t
        entries = AccountingEntry.objects.all()
        assert len(entries) == 2
        assert entries[0].transaction == t
        assert entries[1].transaction == t

        with pytest.raises(ValidationError) as e:
            cr_entry.cr_amount = 8000
            baker.make(
                AccountingTransaction,
                dr_entry=dr_entry,
                cr_entry=cr_entry,
            )

        msg = (
            "Transaction does not observe double entry. "
            "Cash (dr) - 10000.00 != Bank (cr) - 8000"
        )
        assert msg in e.value.messages[0]

    def test_ac_entry(self, currency):
        """Test correct account double entry."""
        account = baker.make(Account, name="Bank")
        entry = baker.prepare(
            AccountingEntry,
            account=account,
            dr_amount=20000,
            currency=currency,
        )
        matching_entry = baker.prepare(
            AccountingEntry,
            cr_amount=20000,
            account=baker.make(Account),
            currency=currency,
        )

        # Create entries via a transaction
        t = baker.make(
            AccountingTransaction,
            dr_entry=entry,
            cr_entry=matching_entry,
        )

        entry.refresh_from_db()
        assert str(entry) == "Bank Ksh 20000.00000000"

        # test values
        assert entry.dr_value == 20000
        assert entry.cr_value == 0
        currency_two = baker.make(Currency, name="USD", conversion_rate=100)
        entry.currency = currency_two
        entry.save()
        entry.refresh_from_db()
        assert entry.dr_value == 2_000_000
        assert entry.amount == 2_000_000

        # validation
        # validate amount
        with pytest.raises(ValidationError) as e:
            baker.make(
                AccountingEntry,
                dr_amount=2000,
                cr_amount=1000,
                currency=currency,
                transaction=t,
            )

        msg = (
            "An account entry can only be a dr entry or a cr entry "
            "at any given time. Kindly provide either of dr_amount or "
            "cr_amount and not both of them"
        )
        assert msg in e.value.messages[0]

    def test_account_balance(self, currency):
        """Test account balance."""
        parent_account = baker.make(
            Account, is_control_account=True, heading__balance_type="dr"
        )
        account = baker.make(
            Account, heading=parent_account.heading, parent=parent_account
        )
        entry_recipe = Recipe(
            AccountingEntry,
            currency=currency,
        )
        entry = entry_recipe.prepare(dr_amount=20000, account=account)
        matching_entry = entry_recipe.prepare(
            cr_amount=20000, account=baker.make(Account)
        )

        baker.make(
            AccountingTransaction,
            dr_entry=entry,
            cr_entry=matching_entry,
        )

        assert account.dr_total() == 20000
        assert account.cr_total() == 0
        assert account.balance() == 20000

        # set two
        entry_two = entry_recipe.prepare(dr_amount=10000, account=account)
        matching_entry_two = entry_recipe.prepare(
            cr_amount=10000, account=baker.make(Account)
        )

        baker.make(
            AccountingTransaction,
            dr_entry=entry_two,
            cr_entry=matching_entry_two,
        )

        assert account.dr_total() == 30000
        assert account.cr_total() == 0
        assert account.balance() == 30000

        entry_three = entry_recipe.prepare(cr_amount=15000, account=account)
        matching_entry_three = entry_recipe.prepare(
            dr_amount=15000, account=baker.make(Account)
        )

        baker.make(
            AccountingTransaction,
            dr_entry=entry_three,
            cr_entry=matching_entry_three,
        )

        assert account.dr_total() == 30000
        assert account.cr_total() == 15000
        assert account.balance() == 15000

        assert parent_account.dr_total() == 30000
        assert parent_account.cr_total() == 15000
        assert parent_account.balance() == 15000

        # test with account balance type cr
        account.heading.balance_type = "cr"
        account.heading.save()
        assert account.dr_total() == 30000
        assert account.cr_total() == 15000
        assert account.balance() == -15000
