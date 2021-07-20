from django.db import models


#exchange: valor de cotización de moneda
#fee_percentage: porcentaje de flete

#nota: 
# 1. exchange USD = 1 para los datos burndown (Quemado, atogenerados..etc), por ser la moneda base
# el resto de valores son aleatorios (que por efecto de practicidad use de google *USD TO CAD*)

#La función de la clase Currency es poder almacenar monedas
class Currency(models.Model):
    id_currency = models.AutoField(primary_key=True)
    name = models.CharField(max_length=4)
    exchange = models.FloatField()
    fee_percentage = models.FloatField()
    quantity = models.FloatField()
        

    def __str__(self):
        return super().__str__()


#La función de la clase Track_Fee es poder almacenar todas las transacciones
class Track_Fee(models.Model):
    id_track_fee = models.AutoField(primary_key=True)
    fee_amount = models.FloatField()
    money_request = models.FloatField()
    date_transaction = models.CharField(max_length=45)
    base_currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, related_name='base')
    quote_currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, related_name='quote')

    def __str__(self):
        return super().__str__()
