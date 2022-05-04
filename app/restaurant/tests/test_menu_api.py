from rest_framework import status
from rest_framework.test import APIClient

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from core.models import Restaurant, Menu

from restaurant.serializers import MenuSerializer


MENU_URL = reverse('restaurant:menu-list')


def sample_restaurant(name):
    return Restaurant.objects.create(name=name)


def sample_menu(restaurant, menu_day):
    return Menu.objects.create(restaurant=restaurant, menu_day=menu_day)


def create_superuser(email, password):
    return get_user_model().objects.create_superuser(email, password)


class PublicMenuAPITests(TestCase):
    """Test unauthenticated API access"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required_to_list(self):
        """Test that authentication is required to list menu objects"""
        res = self.client.get(MENU_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateMenuAPITests(TestCase):
    """Test authentication API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)
        self.restaurant = sample_restaurant(name='Panda Express')

    def test_retrieve_menus(self):
        """Test retrieving a list of menus"""
        sample_menu(restaurant=self.restaurant, menu_day='M')
        sample_menu(restaurant=self.restaurant, menu_day='T')

        superuser = create_superuser(
            email='admin@admin.com',
            password='admin'
        )
        self.client.force_authenticate(superuser)

        res = self.client.get(MENU_URL)

        menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)

    def test_user_create_menu_fails(self):
        """Test that the user can not create a menu objects"""
        payload = {
            'restaurant': self.restaurant,
            'menu_day': 'TH'
        }
        res = self.client.post(MENU_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_invalid_menu_fails(self):
        """Test creating invalid menu fails"""
        payload = {
            'restaurant': '',
            'menu_day': ''
        }
        superuser = create_superuser(
            email='admin@admin.com',
            password='admin'
        )
        self.client.force_authenticate(superuser)
        res = self.client.post(MENU_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
