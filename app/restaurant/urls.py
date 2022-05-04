from django.urls import path
from .views import ListRestaurantView, CreateRestaurantView

app_name = 'restaurant'

urlpatterns = [
    path('restaurant-list', ListRestaurantView.as_view(), name='restaurant-list'),
    path('restaurant-create', CreateRestaurantView.as_view(),
         name='restaurant-create')
]
