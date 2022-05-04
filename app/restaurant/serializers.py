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
        fields = ('id', 'restaurant', 'menu_day', 'image')
        read_only_fields = ('id',)


class MenuDetailSerializer(MenuSerializer):
    """Serialize a menu detail"""
    restaurant = RestaurantSerializer(read_only=True)


class MenuImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to menu"""

    class Meta:
        model = Menu
        fields = ('id', 'image')
        read_only_fields = ('id',)
