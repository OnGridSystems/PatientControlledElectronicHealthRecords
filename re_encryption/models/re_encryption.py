from django.db import models

from re_encryption.models.records_set import RecordsSet


class ReEncryption(models.Model):
    records_set = models.ForeignKey(RecordsSet, on_delete=models.CASCADE)
    verifying_key = models.CharField(max_length=200, blank=True, null=True)
    recepient_id = models.IntegerField()
