from django.urls import path, include
from .views import ListRestaurantView, CreateRestaurantView, ListMenuView,  MenuViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('menus', MenuViewSet)

app_name = 'restaurant'

urlpatterns = [
    path('restaurant-list', ListRestaurantView.as_view(), name='restaurant-list'),
    path('restaurant-create', CreateRestaurantView.as_view(),
         name='restaurant-create'),
    path('employee/menu-list', ListMenuView.as_view(), name='menu-list'),
    # path('menu-create', CreateMenuView.as_view(), name='menu-create'),
    # path('menu-retrieve/<int:id>', DetailMenuView.as_view(), name='menu-retrieve'),
    path('', include(router.urls))
]
