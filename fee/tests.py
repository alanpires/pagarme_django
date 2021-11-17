from django.test import TestCase


class TestFeeGenericView(TestCase):
    def setUp(self):
        self.fee_data = {
            "credit_fee": 5,
            "debit_fee": 3
        }
    
    def test_create_fee(self):
        response = self.client.post('/api/fee/', self.fee_data, format='json')
        
        self.assertEqual(response.json(),
                         {
                            "id": 1,
                            "credit_fee": 5,
                            "debit_fee": 3  
                         }
                        )
        
        self.assertEqual(response.status_code, 201)
    
    def test_get_fee(self):
        create_fee = self.client.post('/api/fee/', self.fee_data, format='json')
        
        response = self.client.get('/api/fee/', format='json')
        
        self.assertEqual(response.json(),
                         [
                             {
                                 "id": 1,
                                 "credit_fee": 5,
                                 "debit_fee": 3
                             }
                         ])
        
        self.assertEqual(response.status_code, 200)
    
    def test_create_many_fees(self):
        # create 3 fees
        for _ in range(3):
            create_fee = self.client.post('/api/fee/', self.fee_data, format='json')
        
        response = self.client.get('/api/fee/', format='json')
        
        self.assertEqual(response.json(),
                         [
                             {
                                 "id": 1,
                                 "credit_fee": 5,
                                 "debit_fee": 3
                             },
                             {
                                 "id": 2,
                                 "credit_fee": 5,
                                 "debit_fee": 3
                             },
                             {
                                 "id": 3,
                                 "credit_fee": 5,
                                 "debit_fee": 3
                             }
                         ]
                         )
        
        self.assertEqual(len(response.json()), 3)
        
        self.assertEqual(response.status_code, 200)