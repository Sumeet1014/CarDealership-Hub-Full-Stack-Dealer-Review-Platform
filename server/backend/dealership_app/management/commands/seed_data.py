import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from dealership_app.models import CarMake, CarModel, Dealer, Review


DEALERS = [
    {
        'name': 'Kansas City Auto',
        'address': '123 Main St',
        'city': 'Kansas City',
        'state': 'KS',
        'zip': '64101',
        'phone': '816-555-0101',
        'website': 'https://kansascityauto.example.com',
        'image': 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d',
        'description': 'Kansas City dealership',
    },
    {
        'name': 'Wichita Cars',
        'address': '456 Oak Ave',
        'city': 'Wichita',
        'state': 'KS',
        'zip': '67202',
        'phone': '316-555-0202',
        'website': 'https://wichitacars.example.com',
        'image': 'https://images.unsplash.com/photo-1492144534655-ae79c964c9d7',
        'description': 'Wichita dealership',
    },
]

CAR_MAKES = {
    'Toyota': ['Camry', 'Corolla', 'RAV4'],
    'Honda': ['Civic', 'Accord', 'CR-V'],
    'Ford': ['Mustang', 'Explorer', 'F-150'],
    'Nissan': ['Altima', 'Sentra'],
    'Chevrolet': ['Malibu', 'Equinox'],
}

REVIEWS = [
    {
        'dealer': 'Kansas City Auto',
        'review_text': 'Fantastic services',
        'rating': 5,
        'sentiment': 'positive',
    },
    {
        'dealer': 'Wichita Cars',
        'review_text': 'Excellent dealership and very helpful staff',
        'rating': 5,
        'sentiment': 'positive',
    },
]

DEFAULT_DEMO_USERNAME = 'testuser'
DEFAULT_DEMO_EMAIL = 'test@test.com'


class Command(BaseCommand):
    help = (
        'Idempotently seed the Cars Dealership data (dealers, car makes/models, '
        'demo user and reviews). Safe to run on every deployment.'
    )

    def handle(self, *args, **options):
        seed_user = self._get_or_create_seed_user()

        with transaction.atomic():
            dealer_created = self._seed_dealers()
            make_created, model_created = self._seed_cars()
            review_created = self._seed_reviews(seed_user)

        self.stdout.write(
            self.style.SUCCESS(
                'Seed complete: '
                f'{dealer_created} dealer(s), '
                f'{make_created} car make(s), '
                f'{model_created} car model(s), '
                f'{review_created} review(s) created; '
                f'{Dealer.objects.count()} dealer(s), '
                f'{CarMake.objects.count()} car make(s), '
                f'{CarModel.objects.count()} car model(s), '
                f'{Review.objects.count()} review(s) total.'
            )
        )

    def _get_or_create_seed_user(self):
        username = os.environ.get('SEED_DEMO_USERNAME', '').strip()
        email = os.environ.get('SEED_DEMO_EMAIL', '').strip()
        password = os.environ.get('SEED_DEMO_PASSWORD', '')

        if username or password:
            if not username or not password:
                raise CommandError(
                    'Both SEED_DEMO_USERNAME and SEED_DEMO_PASSWORD must be set '
                    'to create the deployment demo user.'
                )

            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': email or DEFAULT_DEMO_EMAIL},
            )
            changed = created
            if email and user.email != email:
                user.email = email
                changed = True
            # Keep the environment variable as the source of truth without
            # writing the plaintext password anywhere.
            if created or not user.check_password(password):
                user.set_password(password)
                changed = True
            if changed:
                user.save()
            if created:
                action = 'created'
            elif changed:
                action = 'updated'
            else:
                action = 'already exists'
            self.stdout.write(f'Demo user "{username}" {action}.')
            return user

        # Local development may not define the seed credentials. Reuse an
        # existing account so data can still be initialized safely.
        user = User.objects.filter(username=DEFAULT_DEMO_USERNAME).first()
        if user is None:
            user = User.objects.order_by('id').first()
        if user is None:
            raise CommandError(
                'No user exists to own the seeded reviews. Set '
                'SEED_DEMO_USERNAME, SEED_DEMO_EMAIL and SEED_DEMO_PASSWORD '
                'before seeding a fresh database.'
            )

        self.stdout.write(
            f'SEED_DEMO_USERNAME/SEED_DEMO_PASSWORD not set; using existing '
            f'user "{user.username}" for seeded reviews.'
        )
        return user

    def _seed_dealers(self):
        created = 0
        for dealer_data in DEALERS:
            _, was_created = Dealer.objects.get_or_create(
                name=dealer_data['name'],
                defaults={
                    'address': dealer_data['address'],
                    'city': dealer_data['city'],
                    'state': dealer_data['state'],
                    'zip': dealer_data['zip'],
                    'phone': dealer_data['phone'],
                    'website': dealer_data['website'],
                    'image': dealer_data['image'],
                    'description': dealer_data['description'],
                },
            )
            created += int(was_created)
        return created

    def _seed_cars(self):
        makes_created = 0
        models_created = 0
        for make_name, model_names in CAR_MAKES.items():
            make, was_created = CarMake.objects.get_or_create(make=make_name)
            makes_created += int(was_created)
            for model_name in model_names:
                _, model_was_created = CarModel.objects.get_or_create(
                    make=make,
                    model=model_name,
                )
                models_created += int(model_was_created)
        return makes_created, models_created

    def _seed_reviews(self, user):
        created = 0
        for review_data in REVIEWS:
            dealer = Dealer.objects.get(name=review_data['dealer'])
            _, was_created = Review.objects.get_or_create(
                dealer=dealer,
                review_text=review_data['review_text'],
                defaults={
                    'user': user,
                    'rating': review_data['rating'],
                    'sentiment': review_data['sentiment'],
                },
            )
            created += int(was_created)
        return created
