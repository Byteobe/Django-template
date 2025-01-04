from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Settings, UnitOfMeasurement
from .serializers import SettingsSerializer, UnitOfMeasurementSerializer
from rest_framework.decorators import action
from .models import State, City
from .serializers import (
    StateSerializer, CitySerializer, StateWithCitiesSerializer)



@extend_schema(tags=['Settings'])
class ConfigurationView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer

class StateViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = State.objects.all().order_by('id')
    serializer_class = StateSerializer

    def retrieve(self, request, *args, **kwargs):
        return Response(
            {"detail": "Method Not Allowed"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False, methods=['get'])
    def with_cities(self, request, *args, **kwargs):
        permission_classes = [permissions.AllowAny]
        states = State.objects.prefetch_related('cities').all()
        serializer = StateWithCitiesSerializer(states, many=True)
        return Response(serializer.data)


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = City.objects.all().order_by('id')
    serializer_class = CitySerializer

    def retrieve(self, request, *args, **kwargs):
        return Response(
            {"detail": "Method Not Allowed"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED)

class UnitOfMeasurementApi(generics.ListCreateAPIView):
    queryset = UnitOfMeasurement.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UnitOfMeasurementSerializer
