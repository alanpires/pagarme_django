from datetime import datetime, timedelta
from django.test import TestCase
from rest_framework.test import APIClient
from transactions.models import Payable, Transaction
from fee.models import Fee
import calendar
from transactions.services import converted_date
from django.contrib.auth.models import User


class TestTransactionModel(TestCase):
    def setUp(self):
        self.transaction_data = {
            "amount": 100,
            "description": "Smartband XYZ 3.0",
            "payment_method": "credit_card",
            "card_number": "1234000012340000",
            "cardholders_name": "Fulano da Silva",
            "card_expiring_date": "04-2020",
            "cvv": "100",
            "client_id": 1
        }
        
        self.converted_transaction_data = {
            "amount": 100,
            "description": "Smartband XYZ 3.0",
            "payment_method": "credit_card",
            "card_number": "1234000012340000",
            "cardholders_name": "Fulano da Silva",
            "card_expiring_date": datetime.strptime("30-4-2020", "%d-%m-%Y"),
            "cvv": "100",
            "client_id": 1
        }
    
    def test_create_transaction(self):
        # create transaction
        
        # converted_data
        date = converted_date(self.transaction_data['card_expiring_date'])
        
        card_expiring_date = self.transaction_data.pop("card_expiring_date")
        
        transaction = Transaction.objects.create(**self.transaction_data, card_expiring_date=date)
        
        # load transaction
        transaction = Transaction.objects.last()
        
        self.assertIsInstance(transaction, object)
        self.assertIsInstance(transaction.amount, float)
        self.assertIsInstance(transaction.description, str)
        self.assertIsInstance(transaction.payment_method, str)
        self.assertIsInstance(transaction.card_number, str)
        self.assertIsInstance(transaction.cardholders_name, str)
        # self.assertIsInstance(transaction.card_expiring_date, datetime)
        self.assertIsInstance(transaction.cvv, str)
        self.assertIsInstance(transaction.client_id, int)
        
    
class TestTransactionPayables(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.transaction_credit_card_data = {
            "amount": 100,
            "description": "Smartband XYZ 3.0",
            "payment_method": "credit_card",
            "card_number": "1234000012340000",
            "cardholders_name": "Fulano da Silva",
            "card_expiring_date": "04-2020",
            "cvv": "100",
            "client_id": 1
        }
        
        self.fee_data = {
            "credit_fee": 5,
            "debit_fee": 3
        }
        
        self.payable_expected_credit_card = {
            "status": "waiting_funds",
            "amount_client": 95
        }
        
        self.transaction_debit_card_data = {
            "amount": 100,
            "description": "Smartband XYZ 3.0",
            "payment_method": "debit_card",
            "card_number": "1234000012340000",
            "cardholders_name": "Fulano da Silva",
            "card_expiring_date": "04-2020",
            "cvv": "100",
            "client_id": 1
        }
        
        self.payable_expected_debit_card = {
            "status": "paid",
            "amount_client": 97
        }
        
        self.client_data = {
            'username': 'client',
            'email': 'client@123.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': '1234'
        }
    
    def test_create_transaction_with_the_credit_card(self):
        # converted_data
        date = converted_date(self.transaction_credit_card_data['card_expiring_date'])
        
        # remove card_expiring_date to use the format date
        self.transaction_credit_card_data.pop("card_expiring_date")
        
        # create transaction
        transaction = Transaction.objects.create(**self.transaction_credit_card_data, card_expiring_date=date)
        
        # create fee
        fee = Fee.objects.create(**self.fee_data)
        
        # create user
        client_user = User.objects.get_or_create(**self.client_data)
        
        # Get client user
        client = User.objects.get(id=self.transaction_credit_card_data['client_id'])
        
        # create payable
        payable = Payable.objects.create(
            transaction=transaction, 
            fee=fee,
            user=client)
        
        payable.status = payable.define_status()
        payable.payment_date = payable.define_payment_date()
        payable.amount_client = payable.calculate_amount_client()
        payable.save()
        
        self.assertEqual(payable.status, self.payable_expected_credit_card['status'])
        self.assertEqual(payable.amount_client, self.payable_expected_credit_card['amount_client'])
    
    def test_if_the_payment_date_is_d_plus_30_with_the_credit_card(self):
        # converted_data
        date = converted_date(self.transaction_credit_card_data['card_expiring_date'])
        
        # remove card_expiring_date to use the format date
        self.transaction_credit_card_data.pop("card_expiring_date")
        
        # create transaction
        transaction = Transaction.objects.create(**self.transaction_credit_card_data, card_expiring_date=date)
        
        # create fee
        fee = Fee.objects.create(**self.fee_data)
        
        # create user
        client_user = User.objects.get_or_create(**self.client_data)
        
        # Get client user
        client = User.objects.get(id=self.transaction_credit_card_data['client_id'])
        
        # create payable
        payable = Payable.objects.create(
            transaction=transaction, 
            fee=fee,
            user=client
            )
        
        payable.status = payable.define_status()
        payable.payment_date = payable.define_payment_date()
        payable.amount_client = payable.calculate_amount_client()
        payable.save()
        
        current_date = transaction.date_transaction
        date_payable = payable.payment_date
        delta_between_dates = (date_payable - current_date).days
        
        self.assertEqual(delta_between_dates, 30)
    
    def test_create_transaction_with_the_debit_card(self):
        # converted_data
        date = converted_date(self.transaction_debit_card_data['card_expiring_date'])
        
        # remove card_expiring_date to use the format date
        self.transaction_debit_card_data.pop("card_expiring_date")
        
        # create transaction
        transaction = Transaction.objects.create(**self.transaction_debit_card_data, card_expiring_date=date)
        
        # create fee
        fee = Fee.objects.create(**self.fee_data)
        
        # create user
        client_user = User.objects.get_or_create(**self.client_data)
        
        # Get client user
        client = User.objects.get(id=self.transaction_credit_card_data['client_id'])
        
        # create payable
        payable = Payable.objects.create(
            transaction=transaction, 
            fee=fee,
            user=client)
        
        payable.status = payable.define_status()
        payable.payment_date = payable.define_payment_date()
        payable.amount_client = payable.calculate_amount_client()
        payable.save()
        
        self.assertEqual(payable.status, self.payable_expected_debit_card['status'])
        self.assertEqual(payable.amount_client, self.payable_expected_debit_card['amount_client'])
    
    def test_if_the_payment_date_is_d_plus_0_with_the_debit_card(self):
        # converted_data
        date = converted_date(self.transaction_debit_card_data['card_expiring_date'])
        
        # remove card_expiring_date to use the format date
        self.transaction_debit_card_data.pop("card_expiring_date")
        
        # create transaction
        transaction = Transaction.objects.create(**self.transaction_debit_card_data, card_expiring_date=date)
        
        # create fee
        fee = Fee.objects.create(**self.fee_data)
        
        # create user
        client_user = User.objects.get_or_create(**self.client_data)
        
        # Get client user
        client = User.objects.get(id=self.transaction_credit_card_data['client_id'])
        
        # create payable
        payable = Payable.objects.create(
            transaction=transaction, 
            fee=fee,
            user=client)
        
        payable.status = payable.define_status()
        payable.payment_date = payable.define_payment_date()
        payable.amount_client = payable.calculate_amount_client()
        payable.save()
        
        current_date = transaction.date_transaction
        date_payable = payable.payment_date
        delta_between_dates = (date_payable - current_date).days
        
        self.assertEqual(delta_between_dates, 0)
    
    def test_if_is_not_possible_create_transaction_without_available_fee(self):
        # create transaction
        transaction = self.client.post('/api/transactions/', self.transaction_credit_card_data, format='json')
        self.assertEqual(transaction.status_code, 404)
        self.assertEqual(transaction.json(), {'msg': 'no fee available'})
    
    def test_if_is_not_possible_create_transaction_without_created_client_id(self):
        # create fee
        fee = self.client.post('/api/fee/', self.fee_data, format='json')
        
        self.assertEqual(fee.status_code, 201)
        
        # create transaction
        transaction = self.client.post('/api/transactions/', self.transaction_credit_card_data, format='json')
        
        self.assertEqual(transaction.status_code, 404)
    
    def test_post_transaction(self):
        # create fee
        fee = self.client.post('/api/fee/', self.fee_data, format='json')
        
        # create user
        user = self.client.post('/api/accounts/', self.client_data, format='json')
        
        self.assertEqual(user.status_code, 201)
        
        # create transaction
        transaction = self.client.post('/api/transactions/', self.transaction_credit_card_data, format='json')
        
        self.assertEqual(transaction.status_code, 201)
    
    def test_get_transactions(self):
        # create fee
        fee = self.client.post('/api/fee/', self.fee_data, format='json')
        
        # create user
        user = self.client.post('/api/accounts/', self.client_data, format='json')
        
        # create 10 transactions
        for _ in range(10):
            self.client.post('/api/transactions/', self.transaction_credit_card_data, format='json')
        
        # get transactions
        transactions = self.client.get('/api/transactions/', format='json')

        self.assertEqual(len(transactions.json()), 10)
        self.assertEqual(transactions.status_code, 200)
    
    def tests_whether_only_the_last_four_digits_of_the_card_have_been_saved(self):
        # create fee
        fee = self.client.post('/api/fee/', self.fee_data, format='json')
        
        # create user
        user = self.client.post('/api/accounts/', self.client_data, format='json')
        
        # create transaction
        transaction = self.client.post('/api/transactions/', self.transaction_credit_card_data, format='json').json()
        
        self.assertEqual(len(transaction['card_number']), 4)