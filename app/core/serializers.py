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