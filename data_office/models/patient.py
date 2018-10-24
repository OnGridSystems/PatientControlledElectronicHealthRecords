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
    pub_key = models.CharField(max_length=200)

    @property
    def username(self):
        return self.user.username
    
    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def email(self):
        return self.user.email
    
    @username.setter
    def username(self, value):
        self.user.username = value
        self.user.save()