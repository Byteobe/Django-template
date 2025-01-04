from django.contrib import admin
from .models import  CodeRecoverPassword



@admin.register(CodeRecoverPassword)
class CodeRecoverPasswordAdmin(admin.ModelAdmin):
    list_display = ('code', 'user_id')
    readonly_fields = ('code', 'user_id', 'created', 'expiration')