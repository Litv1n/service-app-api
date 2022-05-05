from django.urls import path, include
from .views import VoteView, ListMenuView,  MenuViewSet, ListCurrentDayMenu, MenuEmployeeDetailView, TopMenuCurrentDayView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('menus', MenuViewSet)

app_name = 'menu'


urlpatterns = [
    path('menu-list', ListMenuView.as_view(), name='menu-list'),
    path('current-day-menu/<str:day>',
         ListCurrentDayMenu.as_view(), name='current-day-menu'),
    path('menu-list/<int:pk>',
         MenuEmployeeDetailView.as_view(), name='menu-detail-view'),
    path('menu-list/vote',
         VoteView.as_view(), name='menu-vote'),
    path('top-menu/<str:day>', TopMenuCurrentDayView.as_view(),
         name='top-current-day-menu'),
    path('', include(router.urls))
]
