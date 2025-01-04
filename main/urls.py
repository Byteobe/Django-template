# general imports
from os.path import basename

from django.urls import path
from django.urls import include
from main.views import home
from rest_framework import routers
from main.api import ConfigurationView, StateViewSet, CityViewSet, UnitOfMeasurementApi

# api urls
configurations_api_router = routers.DefaultRouter()
location_api_router = routers.DefaultRouter()

configurations_api_router.register('', ConfigurationView, basename='configurations')
location_api_router.register(r'states', StateViewSet, basename='state')
location_api_router.register(r'cities', CityViewSet, basename='city')

apiurls = ([
    path('configurations/', include(configurations_api_router.urls)),
    path('location/', include(location_api_router.urls)),
    path('unitOfMeasurement/', UnitOfMeasurementApi.as_view(), name='unitOfMeasurement'),
], 'main')


urlpatterns = [
    path('', home, name='home'),
]
