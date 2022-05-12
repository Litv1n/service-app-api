from django.urls import path, include
from .views import RestaurantViewSet

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('restaurants', RestaurantViewSet)

app_name = 'restaurant'

urlpatterns = [
    path('', include(router.urls)),
]
