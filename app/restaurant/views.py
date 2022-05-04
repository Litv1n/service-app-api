from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from core.models import Restaurant
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
