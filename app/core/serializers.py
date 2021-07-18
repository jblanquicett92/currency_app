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
