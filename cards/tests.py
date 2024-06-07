from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Card
import random

class CardTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_card_creation_valid(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post('/api/cards/', {
            'title': 'Test Card',
            'card_number': '1122334455667788',
            'ccv': 103
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Card.objects.filter(user=self.user).exists())

    def test_card_creation_invalid(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post('/api/cards/', {
            'title': 'Test Card',
            'card_number': '1122334455667788',
            'ccv': 102
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_performance(self):
        self.client.login(username='testuser', password='testpass')
        card_numbers = ["".join([str(random.randint(0, 9)) for _ in range(16)]) for _ in range(100)]
        ccv_numbers = [random.randint(100, 999) for _ in range(100)]
        for card_number, ccv in zip(card_numbers, ccv_numbers):
            response = self.client.post('/api/cards/', {
                'title': 'Test Card',
                'card_number': card_number,
                'ccv': ccv
            })
            self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])
