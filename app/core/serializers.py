from rest_framework import serializers
from .models import Currency, Track_Fee


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency

        #ocultando id_currency, por seguridad
        exclude = ('id_currency',)

#Clase para relacionar llaves y valores en formato JSON que 
#requiero a través del metodo POST para crear un trackfee
class Track_Fee_Formatted_Serializer(serializers.Serializer):
    
    money_request = serializers.FloatField(max_value=1000, min_value=1)
    base = serializers.CharField(max_length=4, allow_blank=False)
    quote = serializers.CharField(max_length=4, allow_blank=False)


    class Meta:
        fields = ('base', 'quote', 'money_request')

#Clase para relacionar llave y valor en formato JSON 
#para generar un conjunto de monedas[usd, jpy, eur... n+1] ,
#el valor de generate debe ser True, para que tenga efecto
class setup_Serializer(serializers.Serializer):  

    generate = serializers.BooleanField(required=True)

    class Meta:

        fields = ('generate' )