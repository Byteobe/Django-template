# general imports
from os.path import basename

from django.urls import path
from django.urls import include
from main.views import home
from rest_framework import routers
from main.api import ConfigurationView

# api urls
configurations_api_router = routers.DefaultRouter()

configurations_api_router.register('', ConfigurationView, basename='configurations')

apiurls = ([
    path('configurations/', include(configurations_api_router.urls)),
], 'main')


urlpatterns = [
    path('', home, name='home'),
]
