from django.test import TestCase
from rest_framework.test import APIClient


class TestPayableView(TestCase):
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
        
        self.client_data = {
            'username': 'client',
            'email': 'client@123.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': '1234'
        }
        
        self.client_login_data = {
            'username': 'client',
            'password': '1234'
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
        
        
    def test_if_amount_payable_is_right(self):
        # create fee
        fee = self.client.post('/api/fee/', self.fee_data, format='json')
        
        # create user
        user = self.client.post('/api/accounts/', self.client_data, format='json')
        
        # login
        token = self.client.post('/api/login/', self.client_login_data, format='json').json()['token']
        
        # authorization
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        # create 10 transactions with the credit_card
        for _ in range(10):
            self.client.post('/api/transactions/', self.transaction_credit_card_data, format='json')
            self.client.post('/api/transactions/', self.transaction_debit_card_data, format='json')
        
        # verify amount_payable
        payable = self.client.get('/api/payables/', format='json')
        
        self.assertEqual(payable.status_code, 200)
        self.assertEqual(payable.json()['payable_amount_available'], 970)
        self.assertEqual(payable.json()['payable_amount_waiting_funds'], 950)

