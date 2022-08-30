from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import ImageSerializer
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes as perm_classes
from django.db.models import Q
from .models import Image


class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]
    queryset = Image.objects.all()

    def get_queryset(self):
        lookups = Q(user=self.request.user)
        queryset = self.queryset.filter(lookups)
        return queryset

    @perm_classes([IsAdminUser])
    @action(detail=False, methods=['get'])
    def delete_all(self):
        try:
            Image.objects.all().delete()
            return Response('all images deleted!')
        except Exception as e:
            return Response(e)




