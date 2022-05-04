from rest_framework import serializers

from core.models import Restaurant, Menu


class RestaurantSerializer(serializers.ModelSerializer):
    """Serializer for restaurant objects"""

    class Meta:
        model = Restaurant
        fields = ('id', 'name',)
        read_only_fields = ('id',)


class MenuSerializer(serializers.ModelSerializer):
    """Serializer for the menu objects"""

    class Meta:
        model = Menu
        fields = ('id', 'restaurant', 'menu_day')
        read_only_fields = ('id',)
