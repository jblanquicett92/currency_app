from rest_framework import serializers
from .models import Currency, Track_Fee

class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency

        exclude = ('id_currency',)


class Track_FeeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Track_Fee

        exclude = ('id_track_fee',)
        depth = 1

class Track_Fee_Formatted_Serializer(serializers.ModelSerializer):
    
    money_request = serializers.FloatField(max_value=1000, min_value=1)

    base = serializers.CharField(max_length=4, allow_blank=False)
    quote = serializers.CharField(max_length=4, allow_blank=False)


    class Meta:
        model = Track_Fee
        fields = ('base', 'quote', 'money_request')

class Track_Fee_GetFormatted_Serializer(serializers.ModelSerializer):
    

    fee_amount = serializers.FloatField(max_value=1000, min_value=1)
    money_request = serializers.FloatField(max_value=1000, min_value=1)
    date_transaction = serializers.CharField(max_length=45, allow_blank=False)
    base = serializers.CharField(max_length=4, allow_blank=False)
    quote = serializers.CharField(max_length=4, allow_blank=False)




    class Meta:
        model = Track_Fee
        fields = ('fee_amount', 'money_request', 'date_transaction' , 'base', 'quote', )

class setup_Serializer(serializers.Serializer):
    

    generate = serializers.BooleanField(required=True)

    class Meta:

        fields = ('generate' )