from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from core.models import Restaurant, Menu
from restaurant import serializers


class ListRestaurantView(generics.ListAPIView):
    """List restaurant objects"""
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = Restaurant.objects.all()
    serializer_class = serializers.RestaurantSerializer

    def get_queryset(self):
        """Return restaurant objects ordering by name"""
        return self.queryset.order_by('name')


class CreateRestaurantView(generics.CreateAPIView):
    """Create restaurant objects"""
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAdminUser, )
    queryset = Restaurant.objects.all()
    serializer_class = serializers.RestaurantSerializer


class ListMenuView(generics.ListAPIView):
    """List menu objects"""
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = Menu.objects.all()
    serializer_class = serializers.MenuSerializer

    def get_queryset(self):
        """Return menus objects ordering by restaurant"""
        return self.queryset.order_by('restaurant')


class CreateMenuView(generics.CreateAPIView):
    """Create menu objects"""
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAdminUser, )
    queryset = Menu.objects.all()
    serializer_class = serializers.MenuSerializer

    def get_queryset(self):
        """Return menus objects ordering by restaurant"""
        return self.queryset.order_by('restaurant')
