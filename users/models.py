from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _



class User(AbstractUser):
    class Status(models.TextChoices):
        ACTIVE = 'AC', _('Activo')
        INITIAL = 'IN', _('Inicio')
        IN_PROGRESS = 'PR', _('En progreso')
        DENIED = 'DN', _('Denegado')
        UNPAID = 'UP', _('Sin pago')

    class StatusDelivery(models.TextChoices):
        WORKING = 'WK', _('Trabajando')
        NOT_WORKING = 'NWK', _('No trabajando')
        AVAILABLE = 'AB', _('Disponible')
        BUSY = 'BS', _('Ocupado')

    email = models.EmailField(unique=True)
    username = models.CharField(unique=True)
    phone = models.CharField(max_length=13, null=True)
    avatar = models.ImageField(_('Imagen'), upload_to='users', null=True, blank=True)
    identification = models.CharField(max_length=30, blank=True)
    status = models.CharField(
        _('Estado'),
        max_length=2,
        choices=Status.choices,
        default=Status.INITIAL,
    )
    status_delivery = models.CharField(
        _('Estado'),
        max_length=3,
        choices=StatusDelivery.choices,
        default=StatusDelivery.NOT_WORKING,
    )
    created = models.DateTimeField(
        _('Fecha de creación'),
        auto_now_add=True,
        help_text='Date time on which the object was created'
    )
    modified = models.DateTimeField(
        _('Fecha de la última modificación'),
        auto_now=True,
        help_text='Date time on which the object was last modified'
    )
    rates = models.FloatField(default=0)

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        if self.first_name or self.last_name:
            return f'{self.first_name} {self.last_name}'
        elif self.username:
            return self.username
        else:
            return self.email

    def change_status(self, new_status):
        if new_status in dict(self.Status.choices):
            self.status = new_status
            self.save(update_fields=['status', 'modified'])
        else:
            raise ValueError(f"Status '{new_status}' is not valid.")

    class Meta:
        verbose_name = _("Usuario")
        verbose_name_plural = _("Usuarios")
        get_latest_by = 'created'
        ordering = ['-created', '-modified']