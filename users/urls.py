# general imports
from django.urls import path
from django.urls import include
from .api import RegisterAPIView, UserDetailAPIView, CurrentUserAPIView, UpdateImageProfileAPIView, \
    DeliveriesListAPIView

# api urls



apiurls = ([
    path("current/", CurrentUserAPIView.as_view(), name="get-current-user"),
    path("register/", RegisterAPIView.as_view(), name="user-register"),
    path("user/<str:username>/", UserDetailAPIView.as_view(), name="get-user-detail"),
    path('upload-image-profile/<int:pk>', UpdateImageProfileAPIView.as_view(), name='update-image-profile'),
    path('deliveries/', DeliveriesListAPIView.as_view(), name='deliveries-list'),
], 'users')


urlpatterns = [
]
