import random

from django.shortcuts import render

from authentication.models import CodeRecoverPassword


# Create your views here.
def generate_code():
    code = random.randint(100000, 999999)
    try:
        code_validate = CodeRecoverPassword.objects.get(code=code)
        generate_code()
    except CodeRecoverPassword.DoesNotExist:
        return code
