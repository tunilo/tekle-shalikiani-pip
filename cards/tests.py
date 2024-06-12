from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class CardCreationTests(APITestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_create_card_valid(self):
        url = reverse('card-list')
        valid_data = {
            'user': self.user.id,
            'title': 'My Card',
            'card_number': '1122334455667788',
            'ccv': '103'
        }
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(url, valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
