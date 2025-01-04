import jwt
from django.conf import settings
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.db.models import Q
from django.template.loader import render_to_string
from pyasn1.type.univ import Boolean
from rest_framework import  permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response  import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from rest_framework import  permissions, status
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, OpenApiResponse
from django.utils import timezone
import datetime
from datetime import timedelta

from main.serializers import GeneralMessageSerializer
from users.models import User
from users.serializers import RegisterSerializer
from .models import CodeRecoverPassword
from .serializers import CustomTokenObtainPairSerializer, TokenOutputSerializer, LogoutSerializer, \
    ResetPasswordSerializer, ResetPasswordCodeValidateRequestSerializer, ResetPasswordRequestSerializer, \
    UpdatePasswordSerializer, ValidateCodeRequestSerializer, GenerateCredentialsSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group

from .utils import generate_random_string
from .views import generate_code


class TokenObtainAPIView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

    @extend_schema(
        description=_("Iniciar Sesión"),
        responses={200: TokenOutputSerializer},
        methods=["post"]
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            print(e)
            return Response(
                {"detail": _("Credenciales inválidas. Por favor, verifique su nombre de usuario y contraseña.")},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class TokenRefreshAPIView(TokenRefreshView):
    pass

class LogoutAPIView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description=_("Cerrar sesión"),
        request=LogoutSerializer,
        methods=["post"],
        responses={
            200: OpenApiResponse(description=_('Cierre de sesión exitoso')),
            401: OpenApiResponse(description=_('Usted no tiene permiso para ver este usuario')),
        },
    )
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh_token"]
            print(refresh_token)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': _('Sesión cerrada correctamente')}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordCodeApiView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ResetPasswordRequestSerializer

    @extend_schema(tags=['authentication'],
                   summary=_('Generar codigo de seguridad para el cambio de contraeña'),
                   description=_(''),
                    responses=GeneralMessageSerializer(),
               )
    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordRequestSerializer(data=request.data)
        email = request.data['email']
        if serializer.is_valid(raise_exception=False):
            try:
                user = User.objects.get(email=email)
                code = generate_code()
                expiration = timezone.now() + timedelta(minutes=60)
                code_recovery = CodeRecoverPassword.objects.create(
                    user_id=user,
                    code=code,
                    created=timezone.now(),
                    expiration=expiration
                )
                if code_recovery.pk:
                    subject = _("Restablecer Contraseña")
                    html_message = render_to_string('recover password/reset_password_code.html', {
                        'code': code,
                        'first_name': user.first_name,
                    })
                    send_email = send_mail(
                        subject, '',
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=False,
                        html_message=html_message)
                    if send_email > 0:
                        return Response(GeneralMessageSerializer({'message': email}).data, status=status.HTTP_200_OK)
                    else:
                        return Response(GeneralMessageSerializer({'message': _('No se logro enviar el correo')}).data,status=status.HTTP_404_NOT_FOUND)
            except User.DoesNotExist:
                return Response(GeneralMessageSerializer({'message': _('El usuario no existe')}).data, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordCodeVerifyApiView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ResetPasswordCodeValidateRequestSerializer

    @extend_schema(tags=['authentication'] , responses=ValidateCodeRequestSerializer)
    def post(self, request, *args, **kwargs):
        try:
            code_ = request.data['code']
            email = request.data['email']
            user = User.objects.get(email=email)
            code = CodeRecoverPassword.objects.get(code=code_, user_id=user)
            if code is not None:
                if code.expiration > timezone.now():
                    code.delete()
                    payload = {
                        'user_id': user.id,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(
                            days=settings.PASSWORD_RESET_EXPIRE_DAYS),
                        'iat': datetime.datetime.utcnow(),
                    }
                    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                    return Response({'token': token}, status=status.HTTP_200_OK)
                else:
                    return Response({'detail': 'El codigo a caducado'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail': 'El correo es invalido'}, status=status.HTTP_400_BAD_REQUEST)
        except CodeRecoverPassword.DoesNotExist:
            return Response({'detail': 'Codigo invalido'}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['authentication'],
               summary=_('Restablecer la contraseña'),
               description=_('restablecer la contraseña atraves de codigo de seguridad'),
               responses=GeneralMessageSerializer)
class ResetPasswordApiView(APIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            payload = jwt.decode(request.data['token'], settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload['user_id'])
            password_validation.validate_password(request.data['password'])
            encrypted_password = make_password(request.data['password'])
            user.password = encrypted_password
            user.save()
            return Response(GeneralMessageSerializer({'message': 'El cambio de contraseña a sido exitoso!'}).data)
        except jwt.ExpiredSignatureError:
            return Response(GeneralMessageSerializer({'message': 'El token a caducado'}).data)
        except jwt.DecodeError:
            return Response(GeneralMessageSerializer({'message': 'Error del token de seguridad'}).data)
        except User.DoesNotExist:
            return Response(GeneralMessageSerializer({'message': 'El usuario no se encontro'}).data)
        except ValidationError as e:
            return Response(GeneralMessageSerializer({'message': 'La contraseña debe ser mayor a 8 caracteres y contener como minimo una letra'}).data)


class UpdatePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdatePasswordSerializer

    @extend_schema(
        summary=_('Actualizar contraseña'),
        description=_("Actualizar contraseña"),
        request=UpdatePasswordSerializer,
        responses=GeneralMessageSerializer(),
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user
            current_password = serializer.validated_data['current_password']
            new_password = serializer.validated_data['new_password']

            if not user.check_password(current_password):
                return Response(
                    GeneralMessageSerializer({'message': _('La contraseña actual es incorrecta.')}).data,
                    status=status.HTTP_401_UNAUTHORIZED
                )

            try:
                password_validation.validate_password(new_password, user)
            except ValidationError as e:
                return Response(GeneralMessageSerializer({'message': list(e.messages)}).data, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            return Response(
                GeneralMessageSerializer({'message': 'Cambio exitos!'}).data,
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

