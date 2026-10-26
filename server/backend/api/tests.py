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

    def test_create_review_for_authenticated_user(self):
        self.assertTrue(self.client.login(username='tuser', password='tpass123'))
        resp = self.client.post(
            f'/api/dealers/{self.dealer.id}/reviews/',
            {'review_text': 'Fantastic services', 'rating': 5},
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 201)

        review = Review.objects.get(id=resp.json()['id'])
        self.assertEqual(review.dealer, self.dealer)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.review_text, 'Fantastic services')
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.sentiment, 'positive')

    def test_create_review_with_username_fallback(self):
        resp = self.client.post(
            f'/api/dealers/{self.dealer.id}/reviews/',
            {'review_text': 'Great service', 'rating': 4, 'user': 'tuser'},
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 201)

        review = Review.objects.get(id=resp.json()['id'])
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.dealer, self.dealer)
        self.assertEqual(review.review_text, 'Great service')
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.sentiment, 'positive')

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
