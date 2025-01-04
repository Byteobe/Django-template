from django.conf import settings
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field, extend_schema_serializer
from drf_spectacular.types import OpenApiTypes
from django.utils.translation import gettext_lazy as _
from urllib.parse import urljoin
from django.contrib.auth.models import Group


from .models import User




@extend_schema_serializer(component_name="User")
class UserResponseSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    rol = serializers.SerializerMethodField(read_only=True)
    


    @extend_schema_field(OpenApiTypes.STR)
    def get_rol(self, obj):
        rol = ';'.join(rol.name for rol in obj.groups.all())
        return rol

    @extend_schema_field(OpenApiTypes.STR)
    def get_avatar(self, user: User):
        if user.avatar:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(user.avatar.url)
            else:
                return urljoin(settings.BASE_URL, user.avatar.url)
        return ''

    def get_full_name(self, obj):
        return obj.full_name

    class Meta:
        model = User
        fields = ('id', 'avatar', 'rol', 'first_name' , 'last_name', 'email', 'username', 'phone', 'status', 'status_delivery' , 'full_name', 'identification', 'rates')
        

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.RegexField(
        '^(?=.*[a-zA-Z]).{8,}$',  # Expresión regular actualizada
        write_only=True,
        error_messages={
            'invalid': 'La contraseña debe tener al menos 8 caracteres y contener al menos una letra.'
        }
    )
    rol = serializers.CharField(write_only=True)

    
    class Meta:
        model = User
        fields = ['first_name', 'last_name','phone', 'email', 'username','password', 'rol']

    

    def validate_rol(self, value):
        try:
            Group.objects.get(name=value)
        except Group.DoesNotExist:
            raise serializers.ValidationError("El rol especificado no existe.")
        return value

    def create(self, validated_data):
        rol_name = validated_data.pop('rol')
        user = User.objects.create_user(**validated_data)
        rol = Group.objects.get(name=rol_name)
        user.groups.add(rol)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'identification', 'email', 'phone']


class UploadImageProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['avatar',]

