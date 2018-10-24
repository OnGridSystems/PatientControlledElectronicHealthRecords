from django.db import models
from django.contrib.auth.models import User

from users.models.fields import ETHAddressField


class Recepient(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='recepient'
    )

    organisation_id = models.CharField(max_length=100)
    eth_address = ETHAddressField()
    pub_key = models.CharField(max_length=200)
