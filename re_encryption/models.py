from django.db import models

from data_office.models import (
    DataSet,
    Recepient
)


class Delegation(models.Model):
    data_set = models.ForeignKey(
        DataSet,
        on_delete=models.CASCADE,
        related_name='delegations'
    )
    recepient = models.ForeignKey(
        Recepient,
        on_delete=models.CASCADE,
        related_name='delegations'
    )

    delegated_at = models.DateTimeField(auto_now_add=True)


class KeyFragment(models.Model):
    delegation = models.ForeignKey(
        Delegation,
        on_delete=models.CASCADE,
        related_name='key_fragments'
    )

    data = models.BinaryField()
