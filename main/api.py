from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, status, generics
from .models import Settings
from .serializers import SettingsSerializer



@extend_schema(tags=['Settings'])
class ConfigurationView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer
