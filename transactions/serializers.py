from transactions.models import Transaction
from rest_framework import serializers
from .models import Transaction, Fee, Payable


class TransactionSerializer(serializers.ModelSerializer):
    card_expiring_date = serializers.CharField()
    card_number = serializers.CharField()
    class Meta:
        model = Transaction
        fields = '__all__'