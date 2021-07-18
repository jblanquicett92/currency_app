from django.db.utils import DataError
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Currency, Track_Fee
from .serializers import CurrencySerializer, Track_FeeSerializer

from .test import CurrencyTestCase
from django.db import transaction
import datetime


# error_general = openapi.Response(
#         description="",
#         examples={
#             "application/json": {
#                 "detail": "[KeyError], [AttributeError], [DataError], [TypeError], [Exception] [Empty]",

#             }
#         }
# )

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



class Check_exchange_rate(APIView):
    serializer_class =  CurrencySerializer
    
    def get(self, request, base, quote):

        base_upper=base.upper()
        quote_upper=quote.upper()

        if base_upper:

            try:
                base_currency = Currency.objects.get(name=base_upper)
            except Currency.DoesNotExist:
                return Response({'result': 'we couldn’t find the currency'}, status=status.HTTP_404_NOT_FOUND)
            serializer_base = CurrencySerializer(base_currency)
            
        
        if quote_upper:

            try:
                quote_currency = Currency.objects.get(name=quote_upper)
            except Currency.DoesNotExist:
                return Response({'result': 'we couldn’t find the currency'}, status=status.HTTP_404_NOT_FOUND)
            serializer_quote = CurrencySerializer(quote_currency)
        
        print(base_currency.name)
        print(quote_currency.name)

        fee_cost=calc_ex_rate(base_currency, quote_currency)
        base_to_quote=calc_base_to_quote(base_currency, quote_currency)

        print(fee_cost)
        print(base_to_quote)
        
        return Response(
            {
            'result': 'success', 
            'documentation':"http://127.0.0.1:8000/swagger/",
            'current_time': datetime.datetime.now(),
            'base': base_upper,
            'quote': quote_upper,            
            'conversion_rate': base_to_quote,
            'fee_cost':fee_cost,
            }, status=status.HTTP_200_OK)
    

    
class Change_currency(APIView):
    pass

def calc_ex_rate(base_currency, quote_currency):
    fee = base_currency.fee_percentage+quote_currency.fee_percentage
    fee_cost = base_currency.exchange*fee
    formatted_float = "{:.4f}".format(fee_cost)
    return float(formatted_float)

def calc_base_to_quote(base_currency, quote_currency):
    base_to_quote = base_currency.exchange/quote_currency.exchange
    base_to_quote_float = "{:.3f}".format(base_to_quote)
    return float(base_to_quote_float)

@transaction.atomic
def calc_money_to_fulfill_request(money_request, base, quote):
    base_to_quote=calc_base_to_quote(base, quote)
        
    quote_request=base_to_quote*money_request

    new_base = Currency.objects.select_for_update().get(name=base.name)
    new_quote = Currency.objects.select_for_update().get(name=quote.name)

    with transaction.atomic():

        new_base.quantity+=money_request
        new_quote.quantity-=quote_request

        if new_quote.quantity <=0:
            list_new_quantity = [new_base, new_quote]
            return list_new_quantity
        else:
            new_base.save()
            new_quote.save()

            list_new_quantity = [new_base, new_quote]
            print(f'{new_quote.quantity} - {new_base.quantity}')
            return list_new_quantity
    
def create_track_fee(money_request, base, quote):

    money_request_float_format = float(money_request)
    print(money_request_float_format)

    fee_calc=calc_ex_rate(base, quote)
    fee_amount = base.exchange*money_request_float_format*fee_calc
    fee_amount_float_formatted = float("{:.4f}".format(fee_amount))

    tf = Track_Fee.objects.create(
        fee_amount=fee_amount_float_formatted,
        date_transaction=datetime.datetime.now(),
        base_currency=base,
        quote_currency=quote
    )
    return tf