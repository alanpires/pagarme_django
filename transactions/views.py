from rest_framework import serializers
from transactions.serializers import TransactionSerializer
from django.shortcuts import render
from rest_framework.views import APIView
from .models import Transaction, Payable, Fee, PaymentMethodsChoices, StatusChoices
from rest_framework.response import Response
from rest_framework import status
from .services import converted_date
from django.contrib.auth.models import User
from datetime import datetime
from django.shortcuts import get_object_or_404


class TransactionView(APIView):
    def get(self, request):
        transactions = Transaction.objects.all()
        
        serializer = TransactionSerializer(transactions, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # criar transactions
        
        # 1º remover a data do request
        card_expiring_date = serializer.validated_data.pop('card_expiring_date')
        
        # converter data de expiração do cartão
        new_date = converted_date(card_expiring_date)
        
        # o sistema só poderá armazenar e retornar os 4 últimos dígitos do cartão de crédito
        card_number = serializer.validated_data.pop('card_number')
        card_number_modified = card_number[-4:]
        
        # criar transação
        transaction = Transaction.objects.create(**serializer.validated_data, card_expiring_date=new_date, card_number=card_number_modified)
        
        # pegar última taxa cadastrada no sistema        
        fee = Fee.objects.last()
        
        if not fee:
            return Response({'msg': 'no fee available'}, status=status.HTTP_404_NOT_FOUND)
        
        # pegar o usuário da transação conforme client_id da transaction
        client_user = get_object_or_404(User, pk=serializer.validated_data['client_id'])
        
        # criar payable
        payable = Payable.objects.create(
            transaction=transaction,
            fee=fee,
            user=client_user
        )
        
        payable.status = payable.define_status()
        payable.payment_date = payable.define_payment_date()
        payable.amount_client = payable.calculate_amount_client()
        payable.save()
        
        # Não é possível passar um valor de string para o um campo DateField
        # converter de datetime para string
        # transaction.card_expiring_date = transaction.card_expiring_date.strftime("%m-%Y")
        # transaction.save()
        
        serializer = TransactionSerializer(transaction)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)