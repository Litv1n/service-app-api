from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from core.models import Restaurant
from restaurant import serializers


class RestaurantViewSet(viewsets.ModelViewSet):
    """CRUD restaurant objects"""
    authentication_classes = (TokenAuthentication, )
    queryset = Restaurant.objects.all()
    serializer_class = serializers.RestaurantSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
