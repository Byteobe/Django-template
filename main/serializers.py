from urllib.parse import urljoin

from django.conf import settings
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from .models import Settings, Image


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = ['key', 'value']


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = Image
        fields = '__all__'

    @extend_schema_field(OpenApiTypes.STR)
    def get_image(self, image: Image):
        if image.image:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(image.image.url)
            else:
                return urljoin(settings.BASE_URL, image.image.url)
        return ''



class GeneralMessageSerializer(serializers.Serializer):
    message = serializers.CharField()
