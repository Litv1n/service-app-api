from django.urls import path
from .views import ListRestaurantView, CreateRestaurantView, ListMenuView, CreateMenuView

app_name = 'restaurant'

urlpatterns = [
    path('restaurant-list', ListRestaurantView.as_view(), name='restaurant-list'),
    path('restaurant-create', CreateRestaurantView.as_view(),
         name='restaurant-create'),
    path('menu-list', ListMenuView.as_view(), name='menu-list'),
    path('menu-create', CreateMenuView.as_view(), name='menu-create')
]
