from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from fee.models import Fee


class PaymentMethodsChoices(models.TextChoices):
    DEBIT_CARD = 'debit_card', 'debit_card'
    CREDIT_CARD = 'credit_card', 'credit_card'


class Transaction(models.Model):
    amount = models.FloatField()
    description = models.TextField()
    payment_method = models.TextField(choices=PaymentMethodsChoices.choices)
    card_number = models.CharField(max_length=16)
    cardholders_name = models.CharField(max_length=255)
    card_expiring_date = models.DateField(default=timezone.now)
    cvv = models.CharField(max_length=255)
    date_transaction = models.DateTimeField(default=timezone.now)
    client_id = models.IntegerField()


class StatusChoices(models.TextChoices):
    PAID = 'paid', 'paid'
    WAITING_FUNDS = 'waiting_funds', 'waiting_funds'


class Payable(models.Model):
    status = models.CharField(max_length=255, choices=StatusChoices.choices, null=True)
    payment_date = models.DateTimeField(null=True, default=timezone.now)
    amount_client = models.FloatField(null=True)
    transaction = models.OneToOneField(Transaction, on_delete=models.PROTECT)
    fee = models.ForeignKey(Fee, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    
    def define_status(self):
        if self.transaction.payment_method == 'debit_card':
            status = 'paid'
        
        else:
            status = 'waiting_funds'
        
        return status
    
    def define_payment_date(self):
        if self.transaction.payment_method == 'debit_card':
            payment_date = self.transaction.date_transaction
        
        else:
            payment_date = self.transaction.date_transaction + timedelta(days=30)
        
        return payment_date
    
    def calculate_amount_client(self):
        if self.transaction.payment_method == 'debit_card':
            amount_client = self.transaction.amount - self.transaction.amount * self.fee.debit_fee / 100
        
        else:
            amount_client = self.transaction.amount - self.transaction.amount * self.fee.credit_fee / 100
        
        return amount_client
    