from urllib.parse import urljoin

from django.conf import settings
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
<<<<<<< HEAD
from .models import Settings, State, City, Product, Image
=======
from .models import Settings, State, City, Image
>>>>>>> bdcfc6bf379e404483b5edd9b3f28e103448bfd5


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



class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'name']


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']


class StateWithCitiesSerializer(serializers.ModelSerializer):
    cities = CitySerializer(many=True, read_only=True)

    class Meta:
        model = State
        fields = ['id', 'name', 'cities']


<<<<<<< HEAD

class GeneralMessageSerializer(serializers.Serializer):
    message = serializers.CharField()

=======


class GeneralMessageSerializer(serializers.Serializer):
    message = serializers.CharField()
>>>>>>> bdcfc6bf379e404483b5edd9b3f28e103448bfd5
