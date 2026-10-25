from django.db import models
from django.contrib.auth.models import User


class Dealer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=20)
    phone = models.CharField(max_length=50)
    website = models.URLField(max_length=200, blank=True)
    image = models.URLField(max_length=500, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.IntegerField(default=5)
    sentiment = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.dealer.name}'


class CarMake(models.Model):
    id = models.AutoField(primary_key=True)
    make = models.CharField(max_length=100)

    def __str__(self):
        return self.make


class CarModel(models.Model):
    id = models.AutoField(primary_key=True)
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='models')
    model = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.make.make} {self.model}'
