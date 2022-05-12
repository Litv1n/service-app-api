from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.db.models import Max, Q

from core.models import Menu, Vote
from . import serializers


class MenuViewSet(viewsets.ModelViewSet):
    """Retrieve menu object"""
    authentication_classes = (TokenAuthentication, )
    queryset = Menu.objects.all()
    serializer_class = serializers.MenuSerializer

    def get_permissions(self):

        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        current_day_menu = self.request.query_params.get('current-day-menu')
        top_menu = self.request.query_params.get('top-menu')
        queryset = self.queryset

        if current_day_menu:
            return queryset.filter(menu_day=current_day_menu).order_by('-id')
        if top_menu:
            max_votes = queryset.filter(
                menu_day=top_menu
            ).aggregate(Max('votes'))

            return queryset.filter(
                Q(menu_day=top_menu) & Q(votes=max_votes['votes__max'])
            ).order_by('-id')[:1]

        return queryset.order_by('-id')

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
