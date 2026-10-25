from django.test import TestCase, Client
from django.contrib.auth.models import User
from dealership_app.models import Dealer, Review, CarMake, CarModel
import json


class APITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('tuser', 't@test.com', 'tpass123')
        self.dealer = Dealer.objects.create(name='Test Dealer', address='1 St', city='X', state='KS', zip='00000', phone='123')
        self.make = CarMake.objects.create(make='TestMake')
        self.model = CarModel.objects.create(make=self.make, model='TestModel')

    def test_get_dealers(self):
        resp = self.client.get('/api/dealers/')
        self.assertEqual(resp.status_code, 200)

    def test_get_dealer_by_id(self):
        resp = self.client.get(f'/api/dealers/{self.dealer.id}/')
        self.assertEqual(resp.status_code, 200)

    def test_get_dealers_by_state(self):
        resp = self.client.get('/api/dealers/state/KS/')
        self.assertEqual(resp.status_code, 200)

    def test_get_dealer_reviews(self):
        resp = self.client.get(f'/api/dealers/{self.dealer.id}/reviews/')
        self.assertEqual(resp.status_code, 200)

    def test_register(self):
        resp = self.client.post('/api/register/', {'username': 'newuser', 'password': 'newpass123', 'email': 'n@n.com', 'first_name': 'N', 'last_name': 'U'}, content_type='application/json')
        self.assertIn(resp.status_code, [200, 201])

    def test_login_logout(self):
        resp = self.client.post('/api/login/', {'username': 'tuser', 'password': 'tpass123'}, content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post('/api/logout/')
        self.assertEqual(resp.status_code, 200)

    def test_cars(self):
        resp = self.client.get('/api/cars/')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(len(data) > 0)

    def test_analyze_review(self):
        resp = self.client.post('/api/analyze-review/', {'review': 'Fantastic services'}, content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['sentiment'], 'positive')
