from django.test import TestCase
from rest_framework.test import APIClient


class TestAccountView(TestCase):
    def setUp(self):
        self.client = APIClient()
        
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
    
    def test_create_and_login_user(self):
        # created user
        user = self.client.post('/api/accounts/', self.client_data, format='json').json()
        
        self.assertEqual(
            user,
            {
                "id": 1,
                "username": "client",
                "email": "client@123.com",
                "first_name": "John",
                "last_name": "Doe"
            }
        )
        
        # login
        response = self.client.post('/api/login/', self.client_login_data, format='json').json()
        
        self.assertIn('token', response.keys())
    
    def test_create_user_already_exists(self):
        self.client.post('/api/accounts/', self.client_data, format='json')
        
        # create user
        response = self.client.post('/api/accounts/', self.client_data, format='json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'username': ['A user with that username already exists.']})
    
    def test_missing_login_data(self):
        # create user
        self.client.post('/api/accounts/', self.client_data, format='json')
        
        login = self.client.post('/api/login/', {'username': 'critic'}, format='json')
        
        self.assertEqual(login.status_code, 400)
    
    def test_login_with_wrong_credentials(self):
        # create user
        self.client.post('/api/accounts/', self.client_data, format='json')
        
        # login with wrong password
        login = self.client.post('/api/login/', {'username': 'client', 'password': '12345'}, format='json')
        
        self.assertEqual(login.status_code, 401)