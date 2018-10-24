from django.db import models

from users.models.patient import Patient


class RecordsSet(models.Model):
    patient = models.ForeignKey(
        Patient,
        related_name='records_sets',
        on_delete=models.CASCADE
    )
    type = models.CharField(max_length=100)

    data = models.BinaryField()
    capsule = models.BinaryField()
