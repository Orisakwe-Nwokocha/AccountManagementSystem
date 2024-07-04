from rest_framework import serializers

from account.models import Account, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'account', 'amount', 'transaction_type', 'transaction_time',
                  'transaction_status', 'description']


class AccountSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True)

    class Meta:
        model = Account
        fields = ['user', 'account_number', 'account_type', 'balance', 'transactions']
        # transactions = serializers.StringRelatedField


class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['user', 'account_number', 'account_type']


class DepositSerializer(serializers.Serializer):
    account_number = serializers.CharField(max_length=10)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class WithdrawSerializer(serializers.Serializer):
    account_number = serializers.CharField(max_length=10)
    pin = serializers.CharField(max_length=4)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class TransferSerializer(serializers.Serializer):
    sender_account_number = serializers.CharField(max_length=10)
    recipient_account_number = serializers.CharField(max_length=10)
    pin = serializers.CharField(max_length=4)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
