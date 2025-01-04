import logging

from django.contrib.auth.models import Group
from drf_spectacular.utils import extend_schema, extend_schema_serializer, OpenApiResponse
from rest_framework.generics import GenericAPIView
from rest_framework import permissions, status, generics
from rest_framework.response  import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from .serializers import RegisterSerializer, UserResponseSerializer, UserUpdateSerializer, UploadImageProfileSerializer
from .models import User

logger = logging.getLogger(__name__)



@extend_schema(tags=['Users'])
class RegisterAPIView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    @extend_schema(
        summary=_("Registrar un nuevo Usuario"),
        description=_("Registrar un nuevo Usuario"),
        request=RegisterSerializer,
        responses={200: UserResponseSerializer},
        methods=["post"]
    )
    def post(self, request, *args, **kwargs):
        """
        Register a new user and return its details
        """
        email = request.data.get('email')
        username = request.data.get('username')

        existing_user = User.objects.filter(Q(email=email) | Q(username=username)).first()
        if existing_user:
            if existing_user.email == email:
                return Response({'detail': _('Ya existe un usuario con este correo electrónico')}, status=status.HTTP_409_CONFLICT)
            else:
                return Response({'detail': _('Ya existe un usuario con este nombre de usuario')}, status=status.HTTP_409_CONFLICT)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserResponseSerializer(user, context={'request': request}).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Users'])
class UserDetailAPIView(GenericAPIView):
    """
    get:
    Get current user.
    This API resources use API View.
    post:
    Update current user.
    """

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @extend_schema(
        request=UserResponseSerializer,
        summary=_("Obtiene la información de un usuario mediante el nombre usuario"),
        description=_("Obtiene la información de un usuario mediante el nombre usuario"),
        responses={
            200: UserResponseSerializer,
            404: OpenApiResponse(description=_('El Usuario no existe')),
        },
        methods=["get"]
    )
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserResponseSerializer(user, context={'request': request})
        return Response(serializer.data)

    @extend_schema(
        request=UserUpdateSerializer,
        summary=_('Actualizar un usuario'),
        description=_("Actualizar un usario"),
        responses={
            200: UserResponseSerializer,
            404: OpenApiResponse(description=_('El Usuario no existe')),
            400: OpenApiResponse(description=_('Datos inválidos')),
            401: OpenApiResponse(description=_('Usted no tiene permiso para actualizar este usuario')),
        },
        methods=["post"]
    )
    def post(self, request, username):
        if request.user.username == username:
            user = get_object_or_404(User, username=username)
            serializer = UserUpdateSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                user.refresh_from_db()
                serializer = UserResponseSerializer(user, context={'request': request})
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': _("Usted no tiene permiso para actualizar este usuario")},
                            status=status.HTTP_401_UNAUTHORIZED)

    @extend_schema(
        request=UserResponseSerializer,
        summary=_("Elimina un usuario, solo el usuario se puede eliminar a si mismo"),
        description=_("Elimina un usuario, solo el usuario se puede eliminar a si mismo"),
        responses={
            201: OpenApiResponse(description=_('Eliminación exitosa del usuario')),
            404: OpenApiResponse(description=_('El Usuario no existe')),
            400: OpenApiResponse(description=_('Usted no tiene permiso para eliminar este usuario')),
        },
        methods=["delete"]
    )
    def delete(self, request, username):
        # Only can delete yourself
        if request.user.username == username:
            user = get_object_or_404(User, pk=request.user.id)
            # user.status = "DELETED"
            # user.is_active = False
            # delete user data
            user.delete()
            return Response({"status": "OK"})
        else:
            return Response({'detail': _('Usted no tiene permiso para eliminar este usuario')},
                            status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Users'])
class UpdateImageProfileAPIView(generics.GenericAPIView):
    serializer_class = UploadImageProfileSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

    @extend_schema(
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'avatar': {
                        'type': 'string',
                        'format': 'binary'
                    },
                }
            }
        },
        summary=_('Cargar imagen de perfil'),
        description=_("Cargar imagen del perfil"),
        responses={
            200: UserResponseSerializer,
            400: OpenApiResponse(description=_('Datos inválidos')),
            401: OpenApiResponse(description=_('No autorizado')),
        },
        methods=["put"]
    )
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_serializer = UserResponseSerializer(instance, context={'request': request})
        return Response(user_serializer.data)
        

@extend_schema(tags=['Users'])
@extend_schema_serializer(component_name="User")
class CurrentUserAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=["Users"],
        summary=_("Obtiene el Usuario Actual utilizando el token en el HEADER"),
        description=_("Obtiene el Usuario Actual utilizando el token en el HEADER"),
        responses={
            200: UserResponseSerializer,
            401: OpenApiResponse(description=_('Usted no tiene permiso para ver este usuario')),
        },
        methods=["get"]
    )
    def get(self, request):
        """
        Authenticate current user and return his/her details
        """
        current_user = UserResponseSerializer(request.user, context={'request': request})
        logger.info(f"Authenticating current user {request.user.username}")

        return Response(current_user.data)


@extend_schema(tags=["Users"])
class DeliveriesListAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserResponseSerializer

    def get_queryset(self):
        delivery_group = Group.objects.get(name="Delivery")
        return User.objects.filter(groups=delivery_group)





