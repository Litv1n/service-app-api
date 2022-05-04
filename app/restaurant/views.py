from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from core.models import Restaurant, Menu
from restaurant import serializers


class BaseListAttr(generics.ListAPIView):
    """Base view for listing objects"""
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )


class ListRestaurantView(BaseListAttr):
    """List restaurant objects"""
    queryset = Restaurant.objects.all()
    serializer_class = serializers.RestaurantSerializer


class CreateRestaurantView(generics.CreateAPIView):
    """Create restaurant objects"""
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAdminUser, )
    queryset = Restaurant.objects.all()
    serializer_class = serializers.RestaurantSerializer


class ListMenuView(BaseListAttr):
    """List menu objects"""
    queryset = Menu.objects.all()
    serializer_class = serializers.MenuSerializer

    def get_queryset(self):
        """Return menus objects ordering by restaurant"""
        return self.queryset.order_by('restaurant')


class MenuViewSet(viewsets.ModelViewSet):
    """Retrieve menu object"""
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAdminUser, )
    queryset = Menu.objects.all()
    serializer_class = serializers.MenuSerializer

    def get_serializer_class(self):
        if self.action == 'upload_image':
            return serializers.MenuImageSerializer
        elif self.action == 'retrieve':
            return serializers.MenuDetailSerializer

        return self.serializer_class

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a menu"""
        menu = self.get_object()
        serializer = self.get_serializer(
            menu,
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
