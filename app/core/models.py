#Teniendo como descripción primaria (Construcción de API de cambio de divisas)
#Descripciones secundarias:
# 1. Consultar un tipo de cambio
# 2. Cambiar una divisa
# 3. 

from django.db import models

class Currency(models.Model):
    id_currency = models.AutoField(primary_key=True)
    name = models.CharField(max_length=4)
    exchange = models.FloatField()
    fee_percentage = models.FloatField()
    quantity = models.FloatField()
        

    def __str__(self):
        return super().__str__()
    
    def setUp(self):

        XXX=Currency.objects.create(
            name='XXX'.upper(),
            exchange=44,
            fee_percentage=0.0015,
            quantity=1000
        )
        XXX.save()
        

class Track_Fee(models.Model):
    id_track_fee = models.AutoField(primary_key=True)
    fee_amount = models.FloatField()
    money_request = models.FloatField()
    date_transaction = models.CharField(max_length=45)
    base_currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, related_name='base')
    quote_currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, related_name='quote')

    def __str__(self):
        return super().__str__()
