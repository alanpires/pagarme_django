from django.db import models


class Fee(models.Model):
    credit_fee = models.IntegerField()
    debit_fee = models.IntegerField()