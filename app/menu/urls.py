from django.urls import path, include
from .views import VoteView, MenuViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('menus', MenuViewSet)

app_name = 'menu'


urlpatterns = [
    path('menus/vote',
         VoteView.as_view(), name='menu-vote'),
    path('', include(router.urls))
]
