from rest_framework import serializers


class PayableSerializer(serializers.Serializer):
    payable_amount_available = serializers.FloatField()
    payable_amount_waiting_funds = serializers.FloatField()