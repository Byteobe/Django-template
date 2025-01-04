from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


# Create your models here.

class CodeRecoverPassword(models.Model):
    code = models.IntegerField(verbose_name=_('Codigo de seguridad'), null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_created=True)
    expiration = models.DateTimeField(verbose_name=_('tiempo de valido  del codigo'), null=False)

    class Meta:
        verbose_name = _('Codigo de seguridad restablecimiento de contraseña')
        verbose_name_plural = _('Codigos de seguridad restablecimiento de contraseñas')