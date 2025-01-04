from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django_extensions.db.fields import AutoSlugField
from django.utils.translation import gettext_lazy as _



class Settings(models.Model):
    key = models.CharField(max_length=200)
    value = models.CharField(max_length=200)

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = _("Configuración")
        verbose_name_plural = _("Configuraciones")


class Country(models.Model):
    """
    Represents countries.
    """
    name = models.CharField(_("Nombre de País"), max_length=255)
    iso_code = models.CharField(_("ISO Code"), max_length=3, unique=True)  # ISO 3166-1 alpha-3 code
    slug = AutoSlugField(populate_from='name')

    class Meta:
        verbose_name = _("País")
        verbose_name_plural = _("Paises")
        ordering = ("name",)

    def __str__(self):
        return self.name


class State(models.Model):
    """
    Departamentos de Colombia
    """
    country = models.ForeignKey(
        Country, related_name="states",
        null=True,
        on_delete=models.CASCADE,
    )
    name = models.CharField(_("Nombre del Departamento"), max_length=255)
    dane_code = models.CharField(_("Código DANE"), max_length=3)
    geonames_code = models.CharField(_("Código GeoNames"), max_length=10, null=True, blank=True)
    slug = AutoSlugField(populate_from='name')

    @classmethod
    def get_state_by_name(cls, name):
        try:
            return cls.objects.get(name__iexact=name)
        except cls.DoesNotExist:
            print(name)
            return None

    class Meta:
        verbose_name = _("Departamento")
        verbose_name_plural = _("Departamentos")
        ordering = ("name",)

    def __str__(self):
        return self.name


class City(models.Model):
    """
    Ciudades de Colombia
    """
    state = models.ForeignKey(
        State,
        related_name='cities',
        verbose_name=_("Municipios"),
        on_delete=models.CASCADE)
    name = models.CharField(_("Nombre del Municipio"), max_length=255)
    dane_code = models.CharField(_("Código DANE"), max_length=3)
    slug = AutoSlugField(populate_from='name')
    coords_lat = models.FloatField(null=True, blank=True)
    coords_long = models.FloatField(null=True, blank=True)
    geo_location = models.PointField(null=True, blank=True)

    @classmethod
    def get_city_by_name(cls, name, state):
        try:
            if state:
                return cls.objects.get(name__iexact=name, state_id=state.id)
            return cls.objects.get(name__iexact=name)
        except cls.DoesNotExist:
            return None

    class Meta:
        verbose_name = _("Municipios")
        verbose_name_plural = _("Municipios")
        ordering = ("name",)

    def __str__(self):
        return '%s, %s' % (self.name, self.state.name)

    def save(self, *args, **kwargs):
        if self.coords_lat:
            point = Point(self.coords_long, self.coords_lat)
            self.location = point
        super(City, self).save(*args, **kwargs)


class Client(models.Model):
    name = models.CharField(_("Nombre del Cliente"), max_length=255)
    phone = models.CharField(_("Telefone"), max_length=255)

    def __str__(self):
        return self.name


class UnitOfMeasurement(models.Model):
    name = models.CharField(_("Nombre del UnitOfMeasurement"), max_length=255)

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(_("Image"), upload_to="images/")


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    unit_of_measurement = models.ForeignKey(UnitOfMeasurement, on_delete=models.CASCADE)
    units = models.IntegerField(default=1)
    images = models.ManyToManyField(Image, related_name='products', blank=True)

    def __str__(self):
        return self.name


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

