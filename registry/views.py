# from django.shortcuts import render
from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated, \
        IsAdminUser

from registry.models import Registry, \
        Image, \
        Permission

from registry.serializers import RegistrySerializer, \
        ImageSerializer, \
        PermissionSerializer

from registry.permissions import IsImageOwnerOrReadOnly, \
        IsOwnerOrStaffOrReadOnly

class RegistryViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing Docker registry
    """
    queryset = Registry.objects.all()
    serializer_class = RegistrySerializer
    permission_classes = (IsAdminUser,)

class ImageViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing Registry images
    """
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (IsOwnerOrStaffOrReadOnly,)

    def perform_create(self, serializer):
        # https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/#associating-snippets-with-users
        serializer.save(owner=self.request.user)


class PermissionViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing docker image permissions
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = (IsImageOwnerOrReadOnly,)


