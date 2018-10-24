from django.db import models
from django.contrib.auth.models import User

from .fields import ETHAddressField


class Patient(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='patient'
    )

    eth_address = ETHAddressField()
    pub_key = models.CharField(max_length=100)
