# general imports
from django.urls import path
from django.urls import include
from .api import TokenObtainAPIView, TokenRefreshAPIView, LogoutAPIView, ResetPasswordCodeApiView, \
    ResetPasswordCodeVerifyApiView, ResetPasswordApiView, UpdatePasswordAPIView

apiurls = ([
    path('logout/', LogoutAPIView.as_view(), name='user-auth-logout'),
    path('login/', TokenObtainAPIView.as_view(), name="user-login"),
    path('refresh/', TokenRefreshAPIView.as_view(), name="user-refresh-token"),
    path('generate-code', ResetPasswordCodeApiView.as_view(), name="generate code recover password"),
    path('validate-code', ResetPasswordCodeVerifyApiView.as_view(), name="validate recover code "),
    path('recover-password-code', ResetPasswordApiView.as_view(), name="recover password with code"),
    path('update-password/', UpdatePasswordAPIView.as_view(), name="update password"),
], 'authentication')


urlpatterns = [
]
