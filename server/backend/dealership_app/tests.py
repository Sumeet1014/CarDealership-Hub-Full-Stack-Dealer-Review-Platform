import os
from io import StringIO
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from .models import CarMake, CarModel, Dealer, Review


class SeedDataCommandTests(TestCase):
    seed_env = {
        'SEED_DEMO_USERNAME': 'seeduser',
        'SEED_DEMO_EMAIL': 'seed@example.com',
        'SEED_DEMO_PASSWORD': 'seed-password-123',
    }

    def run_seed(self):
        with patch.dict(os.environ, self.seed_env, clear=False):
            call_command('seed_data', stdout=StringIO())

    def test_seed_data_is_idempotent(self):
        self.run_seed()

        counts = {
            'dealers': Dealer.objects.count(),
            'makes': CarMake.objects.count(),
            'models': CarModel.objects.count(),
            'reviews': Review.objects.count(),
            'users': User.objects.count(),
        }
        self.assertEqual(counts['dealers'], 2)
        self.assertEqual(counts['makes'], 5)
        self.assertEqual(counts['models'], 13)
        self.assertEqual(counts['reviews'], 2)
        self.assertEqual(counts['users'], 1)

        self.run_seed()

        self.assertEqual(Dealer.objects.count(), counts['dealers'])
        self.assertEqual(CarMake.objects.count(), counts['makes'])
        self.assertEqual(CarModel.objects.count(), counts['models'])
        self.assertEqual(Review.objects.count(), counts['reviews'])
        self.assertEqual(User.objects.count(), counts['users'])

    def test_seed_user_can_authenticate(self):
        self.run_seed()

        user = User.objects.get(username='seeduser')
        self.assertEqual(user.email, 'seed@example.com')
        self.assertTrue(user.check_password('seed-password-123'))
        self.assertEqual(Review.objects.filter(user=user).count(), 2)

    def test_fresh_database_requires_seed_credentials(self):
        empty_env = {
            'SEED_DEMO_USERNAME': '',
            'SEED_DEMO_EMAIL': '',
            'SEED_DEMO_PASSWORD': '',
        }
        with patch.dict(os.environ, empty_env, clear=False):
            with self.assertRaises(CommandError):
                call_command('seed_data', stdout=StringIO())

        self.assertEqual(Dealer.objects.count(), 0)
        self.assertEqual(User.objects.count(), 0)

    def test_existing_review_is_not_duplicated(self):
        user = User.objects.create_user('existing', 'existing@example.com', 'pass123')
        dealer = Dealer.objects.create(
            name='Kansas City Auto',
            address='123 Main St',
            city='Kansas City',
            state='KS',
            zip='64101',
            phone='816-555-0101',
        )
        Review.objects.create(
            dealer=dealer,
            user=user,
            review_text='Fantastic services',
            rating=5,
            sentiment='positive',
        )

        self.run_seed()

        self.assertEqual(
            Review.objects.filter(
                dealer__name='Kansas City Auto',
                review_text='Fantastic services',
            ).count(),
            1,
        )
