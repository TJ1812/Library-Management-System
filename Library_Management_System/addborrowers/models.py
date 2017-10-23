from __future__ import unicode_literals

from django.db import models

class Borrower(models.Model):
    card_id = models.AutoField(db_column='Card_id', primary_key=True)  # Field name made lowercase.
    ssn = models.CharField(db_column='Ssn', unique=True, max_length=9)  # Field name made lowercase.
    bname = models.CharField(db_column='Bname', max_length=255, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'borrower'