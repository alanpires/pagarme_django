from rest_framework import serializers
from transactions.serializers import TransactionSerializer
from django.shortcuts import render
from rest_framework.views import APIView
from transactions.models import Payable
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .serializers import PayableSerializer
from django.db.models import Sum
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class PayableView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):      
        payable_amount_available = Payable.objects.filter(user=request.user, status='paid').aggregate(amount_paid=Sum('amount_client'))
        payable_amount_waiting_funds = Payable.objects.filter(user=request.user, status='waiting_funds').aggregate(amount_waiting_funds=Sum('amount_client'))

        if payable_amount_waiting_funds['amount_waiting_funds'] == None:
            payable_amount_waiting_funds = {'amount_waiting_funds': 0}
        
        if payable_amount_available['amount_paid'] == None:
            payable_amount_available = {'amount_paid': 0}
        
        serializer = {
            "payable_amount_available": payable_amount_available['amount_paid'],
            "payable_amount_waiting_funds": payable_amount_waiting_funds['amount_waiting_funds']
        }
        
        return Response(serializer, status=status.HTTP_200_OK)