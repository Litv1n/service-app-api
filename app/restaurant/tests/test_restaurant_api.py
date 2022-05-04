from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Restaurant

from restaurant.serializers import RestaurantSerializer


LIST_RESTAURANT_URL = reverse('restaurant:restaurant-list')
CREATE_RESTAURANT_URL = reverse('restaurant:restaurant-create')


def create_superuser(email, password):
    return get_user_model().objects.create_superuser(email, password)


class PublicRestaurantsApiTests(TestCase):
    """Test the publically available restaurant API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required_to_list(self):
        """Test that login is required to access the list restaurant endpoint"""
        res = self.client.get(LIST_RESTAURANT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_to_create(self):
        """Test that login is required to access the create restaurant endpoint"""
        res = self.client.get(CREATE_RESTAURANT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRestaurantAPITests(TestCase):
    """Test restaurants can be retrieved by authorized user and be created by admin"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_restaurants_list(self):
        """Test retrieving a list of restaurants"""
        Restaurant.objects.create(name='Arby"s')
        Restaurant.objects.create(name='Baton Rouge')

        res = self.client.get(LIST_RESTAURANT_URL)

        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_user_create_restaurant_fails(self):
        """Test that user can not create a restaurant objects"""
        payload = {
            'name': 'Baton Rouge'
        }
        res = self.client.post(CREATE_RESTAURANT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_restaurant_successful(self):
        """Test create a new restaurant by admin"""
        superuser = create_superuser(email='admin@admin.com', password='admin')
        self.client.force_authenticate(superuser)
        payload = {
            'name': 'Baton Rouge'
        }

        self.client.post(CREATE_RESTAURANT_URL, payload)
        exists = Restaurant.objects.filter(name=payload['name']).exists()
        self.assertTrue(exists)

    def test_invalid_restaurant_fails(self):
        """Test creating invalid restaurant fails"""
        superuser = create_superuser(email='admin@admin.com', password='admin')
        self.client.force_authenticate(superuser)
        payload = {'name': ''}

        res = self.client.post(CREATE_RESTAURANT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
