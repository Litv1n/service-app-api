from rest_framework import serializers

from core.models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    """Serializer for restaurant objects"""

    class Meta:
        model = Restaurant
        fields = ('id', 'name',)
        read_only_fields = ('id',)
