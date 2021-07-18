from django.db.utils import DataError
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Currency, Track_Fee
from .serializers import CurrencySerializer, Track_FeeSerializer

error_general = openapi.Response(
        description="",
        examples={
            "application/json": {
                "detail": "[KeyError], [AttributeError], [DataError], [TypeError], [Exception] [Empty]",

            }
        }
)

class CurrenciesView(APIView):
    serializer_class =  CurrencySerializer
    
    def is_currency_exists(self, name):
        
        try:
            Currency.objects.get(name=name)
        except Currency.DoesNotExist:
            return False
        return True



    def post(self, request, *args, **kwargs):
        currency_data = request.data
        new_currency = Currency()
        try:
            name_upper=currency_data["name"].upper()
            if self.is_currency_exists(name_upper):
                return Response({'result': 'Currency already exixst'}, status=status.HTTP_400_BAD_REQUEST)
            else:

                new_currency.name = name_upper
                new_currency.exchange = currency_data["exchange"]
                new_currency.fee_percentage = currency_data["fee_percentage"]
                new_currency.quantity = currency_data["quantity"]
            
                new_currency.save()
                serializer = CurrencySerializer(new_currency)
              
        except Exception as ex:
            return Response({'result': ex.args}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'result': 'success', 'new_currency':serializer.data}, status=status.HTTP_201_CREATED)
            

    def get(self, request, name=None):

        if name:

            try:
                queryset = Currency.objects.get(name=name)
            except Currency.DoesNotExist:
                return Response({'result': 'we couldn’t find the currency'}, status=status.HTTP_404_NOT_FOUND)
            serializer = CurrencySerializer(queryset)
            return Response(serializer.data)
        
        else:
            queryset = Currency.objects.all()
            serializer = CurrencySerializer(queryset, many=True)
            return Response(serializer.data)

class exchangeRateView(APIView):
    serializer_class =  CurrencySerializer
    
    def get(self, request, base, quote):

        if base:

            try:
                base_currency = Currency.objects.get(name=base)
            except Currency.DoesNotExist:
                return Response({'result': 'we couldn’t find the currency'}, status=status.HTTP_404_NOT_FOUND)
            serializer_base = CurrencySerializer(base_currency)
            
        
        if quote:

            try:
                quote_currency = Currency.objects.get(name=quote)
            except Currency.DoesNotExist:
                return Response({'result': 'we couldn’t find the currency'}, status=status.HTTP_404_NOT_FOUND)
            serializer_quote = CurrencySerializer(base_currency)
            
        base_to_quote = base_currency.exchange/quote_currency.exchange
        fee = base_currency.fee_percentage+quote_currency.fee_percentage
        fee_cost = base_currency.exchange*fee
        print(quote_currency.name," = ", base_to_quote)
        print(f"fee cost {fee_cost} {base_currency.name}")
        
        
        return Response({'status':1})
