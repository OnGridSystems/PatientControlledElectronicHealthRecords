from django.db import models

from .fields import ETHAddressField


class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    eth_address = ETHAddressField()
    pub_key = models.CharField(max_length=100)


class RecordsSet(models.Model):
    patient = models.ForeignKey(
        Patient,
        related_name="records_sets",
        on_delete=models.CASCADE
    )
    type = models.CharField(max_length=100)

    data = models.BinaryField()
    capsule = models.BinaryField()


class Recepient(models.Model):
    organisation_id = models.CharField(max_length=100)
    eth_address = ETHAddressField()
    pub_key = models.CharField(max_length=100)
    records_sets = models.ManyToManyField(RecordsSet, related_name='recepients')
