from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from core.models import Restaurant
from restaurant import serializers


class BaseListAttr(generics.ListAPIView):
    """Base view for listing objects"""
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )


class ListRestaurantView(BaseListAttr):
    """List restaurant objects"""
    queryset = Restaurant.objects.all()
    serializer_class = serializers.RestaurantSerializer


class CreateRestaurantView(generics.CreateAPIView):
    """Create restaurant objects"""
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAdminUser, )
    queryset = Restaurant.objects.all()
    serializer_class = serializers.RestaurantSerializer
