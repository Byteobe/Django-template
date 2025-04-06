from django.db import models
from django.utils.translation import gettext_lazy as _



class Settings(models.Model):
    key = models.CharField(max_length=200)
    value = models.CharField(max_length=200)

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = _("Configuración")
        verbose_name_plural = _("Configuraciones")

class Image(models.Model):
    image = models.ImageField(_("Image"), upload_to="images/")




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

