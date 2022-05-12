from rest_framework import status
from rest_framework.test import APIClient

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from core.models import Restaurant, Menu
from menu.serializers import MenuSerializer, MenuDetailSerializer


MENU_URL = reverse('menu:menu-list')
VOTE_URL = reverse('menu:menu-vote')


def detail_url(menu_id):
    """Return menu detail for the employee"""
    return reverse('menu:menu-detail', args=[menu_id])


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

    def test_login_required(self):
        """Test that authentication is required to access menu objects"""
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

        menus = Menu.objects.all().order_by('-id')
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

    def test_menu_detail_employee(self):
        """Test detail menu view for employees"""
        menu = sample_menu(restaurant=self.restaurant, menu_day='T')
        url = detail_url(menu.id)

        serializer = MenuDetailSerializer(menu)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_current_day_meny(self):
        """Test that menu objects return for the day in url"""
        monday = 'M'
        sample_menu(restaurant=self.restaurant, menu_day=monday)
        sample_menu(restaurant=self.restaurant, menu_day=monday)

        menus = Menu.objects.filter(menu_day=monday).order_by('-id')
        serializer = MenuSerializer(menus, many=True)

        res = self.client.get(
            MENU_URL,
            {'current-day-menu': monday}
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_menu_success(self):
        """Test creating menu by admin"""
        superuser = create_superuser(
            email='admin@testadmin.com',
            password='adminpass'
        )
        self.client.force_authenticate(superuser)
        payload = {
            'restaurant': self.restaurant.id,
            'menu_day': 'W'
        }

        res = self.client.post(MENU_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_top_menu(self):
        """Test returning top menu of the day"""
        monday = 'M'
        menu1 = Menu.objects.create(
            restaurant=self.restaurant, menu_day='M', votes=10)
        menu2 = Menu.objects.create(
            restaurant=self.restaurant, menu_day='M', votes=5)
        menu3 = Menu.objects.create(restaurant=self.restaurant, menu_day='M')

        res = self.client.get(
            MENU_URL,
            {'top-menu': monday}
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        serializer1 = MenuSerializer(menu1)
        serializer2 = MenuSerializer(menu2)
        serializer3 = MenuSerializer(menu3)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)
