from accounting.models import Account, AccountingEntry
from accounting.models.common import string_date_to_datetime
from rest_framework import serializers


class AccountEntrySerializer(serializers.ModelSerializer):
    """Serialize account entries."""

    balance = serializers.SerializerMethodField()

    def get_balance(self, instance):
        """Get an account entry's corresponding account balance."""
        # `effective_date` for the period filter is not enough
        # since entries from the same document will have
        # same occurrence time; we therefore the need to filter
        # account entries upto this record using `created_by`
        extra_filters = {"created__lte": instance.created}
        return instance.account.balance(
            end=instance.effective_date, extra_filters=extra_filters
        )

    description = serializers.ReadOnlyField(source="accounting_transaction.description")

    class Meta:
        model = AccountingEntry
        fields = "__all__"


class AccountSerializer(serializers.ModelSerializer):
    """Account serializer."""

    account_name = serializers.ReadOnlyField()
    account_heading = serializers.ReadOnlyField(source="heading.heading")
    account_heading_type = serializers.ReadOnlyField(source="heading.heading_type")
    number = serializers.CharField(required=False)
    balance = serializers.SerializerMethodField()
    entries = serializers.SerializerMethodField()

    def get_balance(self, instance):
        """Get an account's balance."""
        end = self.query_params.get("period_1", "")
        end = string_date_to_datetime(end) or instance.current_period.end
        extra_filters = {}
        return instance.balance(end=end, extra_filters=extra_filters)

    def get_entries(self, instance):
        """Get account entries."""
        return [
            AccountEntrySerializer(entry).data
            for entry in instance.account_entries.all()
        ]

    class Meta:
        model = Account
        fields = "__all__"
