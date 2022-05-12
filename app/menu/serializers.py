from rest_framework import serializers

from core.models import Menu, Vote
from restaurant.serializers import RestaurantSerializer


class MenuSerializer(serializers.ModelSerializer):
    """Serializer for the menu objects"""

    class Meta:
        model = Menu
        fields = ('id', 'restaurant', 'menu_day', 'image', 'votes')
        read_only_fields = ('id', 'votes', 'image')


class MenuDetailSerializer(MenuSerializer):
    """Serialize a menu detail"""
    restaurant = RestaurantSerializer(read_only=True)

    class Meta:
        model = Menu
        fields = ('id', 'restaurant', 'menu_day', 'image', 'votes')


class MenuImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to menu"""

    class Meta:
        model = Menu
        fields = ('id', 'image')
        read_only_fields = ('id',)


class VoteSerializer(serializers.ModelSerializer):
    """Serializer for vote objects"""

    class Meta:
        model = Vote
        fields = ('menu',)
        read_only_fields = ('id', 'user')
