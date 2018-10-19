from django.db import models

from .fields import ETHAddressField


class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    eth_address = ETHAddressField()
    pub_key = models.CharField(max_length=100)


class DataSet(models.Model):
    patient = models.ForeignKey(
        Patient,
        related_name="data_sets",
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()

    data = models.BinaryField()
    capsule = models.BinaryField()


class Recepient(models.Model):
    organisation_name = models.CharField(max_length=100)
    eth_address = ETHAddressField()
    pub_key = models.CharField(max_length=100)
    data_sets = models.ManyToManyField(DataSet, related_name='recepients')
