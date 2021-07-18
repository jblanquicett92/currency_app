from rest_framework import serializers
from .models import Currency, Track_Fee

class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ("__all__")


class Track_FeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Track_Fee
        fields = ("__all__")
