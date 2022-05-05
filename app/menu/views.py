from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.db.models import Max, Q

from core.models import Menu, Vote
from restaurant.views import BaseListAttr
from . import serializers


class ListMenuView(BaseListAttr):
    """List menu objects"""
    queryset = Menu.objects.all()
    serializer_class = serializers.MenuSerializer

    def get_queryset(self):
        """Return menus objects ordering by restaurant"""
        return self.queryset.order_by('-id')


class MenuViewSet(viewsets.ModelViewSet):
    """Retrieve menu object"""
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAdminUser, )
    queryset = Menu.objects.all()
    serializer_class = serializers.MenuSerializer

    def get_queryset(self):
        return self.queryset.order_by('-id')

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


class ListCurrentDayMenu(ListMenuView):
    """List menus for the current day"""

    def get_queryset(self):
        day = self.kwargs['day']
        return self.queryset.filter(menu_day=day).order_by('-id')


class MenuEmployeeDetailView(generics.RetrieveAPIView):
    """Menu detail view for employee"""
    authentication_classes = (TokenAuthentication, )
    permissions_classes = (IsAuthenticated, )
    queryset = Menu.objects.all()
    serializer_class = serializers.MenuDetailSerializer


class VoteView(generics.CreateAPIView):
    """Create vote object"""
    authentication_classes = (TokenAuthentication, )
    permissions_classes = (IsAuthenticated, )
    queryset = Vote.objects.all()
    serializer_class = serializers.VoteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        menu_id = serializer.data['menu']
        menu = Menu.objects.get(id=menu_id)
        menu.votes += 1
        menu.save()


class TopMenuCurrentDayView(BaseListAttr):
    queryset = Menu.objects.all()
    serializer_class = serializers.MenuDetailSerializer

    def get_queryset(self):
        day = self.kwargs['day']
        max_votes = Menu.objects.filter(menu_day=day).aggregate(Max('votes'))
        return self.queryset.filter(Q(votes=max_votes['votes__max']) & Q(menu_day=day)).order_by('-id')[0:1]
