from django.db import models


class Currency(models.Model):
    id_currency = models.AutoField(primary_key=True)
    name = models.CharField(max_length=4)
    exchange = models.FloatField()
    fee_percentage = models.FloatField()
    quantity = models.FloatField()

    
    

    def __str__(self):
        return super().__str__()

class Track_Fee(models.Model):
    id_track_fee = models.AutoField(primary_key=True)
    fee_amount = models.FloatField()
    date_transaction = models.CharField(max_length=45)
    base_currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, related_name='base')
    quote_currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, related_name='quote')

    def __str__(self):
        return super().__str__()
