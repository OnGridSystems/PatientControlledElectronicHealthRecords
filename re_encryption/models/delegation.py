from django.db import models

from users.models.recepient import Recepient
from re_encryption.models.records_set import RecordsSet


class Delegation(models.Model):
    records_set = models.ForeignKey(
        RecordsSet,
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

    bytes = models.BinaryField()
