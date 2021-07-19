from django.db.utils import DataError
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from .models import Currency, Track_Fee
from .serializers import CurrencySerializer, Track_FeeSerializer, Track_Fee_Formatted_Serializer, Track_Fee_GetFormatted_Serializer
from .serializers import setup_Serializer

from .setup import AutoGenerateCurrencies

from .test import CurrencyTestCase
from django.db import transaction
import datetime



class Setup(GenericAPIView):
    serializer_class = setup_Serializer
    def post(self, request, *args, **kwargs):

        generate_data = request.data

        generate=generate_data['generate']

        if generate:
            generate_auto_currencies()
            return Response({'result': 'you have generated EUR, USD, JPY, GBP, CHF, AUD, CAD y NZD. currencies'}, status=status.HTTP_201_CREATED)
        return Response({'result': 'unexpected request'}, status=status.HTTP_400_BAD_REQUEST)
    

class CurrenciesView(GenericAPIView):
    serializer_class =  CurrencySerializer
    
    def post(self, request, *args, **kwargs):
        currency_data = request.data
        new_currency = Currency()
        try:
            name_upper=currency_data["name"].upper()
            if is_currency_exists(name_upper):
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
            name_upper=name.upper()
            try:
                queryset = Currency.objects.get(name=name_upper)
            except Currency.DoesNotExist:
                return Response({'result': 'we couldn’t find the currency'}, status=status.HTTP_404_NOT_FOUND)
            serializer = CurrencySerializer(queryset)
            return Response(serializer.data)
        
        else:
            queryset = Currency.objects.all()
            serializer = CurrencySerializer(queryset, many=True)
            return Response(serializer.data)



class Check_exchange_rateView(GenericAPIView):
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
        
        #print(base_currency.name)
        #print(quote_currency.name)

        fee_cost=calc_ex_rate(base_currency, quote_currency)
        base_to_quote=calc_base_to_quote(base_currency, quote_currency)

        #print(fee_cost)
        #print(base_to_quote)
        
        return Response(
            {
            'result': 'success', 
            'documentation':"http://127.0.0.1:8000/redoc/",
            'current_time': datetime.datetime.now(),
            'base': base_upper,
            'quote': quote_upper,            
            'conversion_rate': base_to_quote,
            'fee_cost':fee_cost,
            }, status=status.HTTP_200_OK)
    

    
class Change_currency(GenericAPIView):
    serializer_class = Track_Fee_Formatted_Serializer
    def post(self, request, *args, **kwargs):
        change_currency_data = request.data
        base_upper=change_currency_data['base'].upper()
        quote_upper=change_currency_data['quote'].upper()
        if is_currency_exists(base_upper) and is_currency_exists(quote_upper):
            base = Currency.objects.get(name=base_upper)
            quote = Currency.objects.get(name=quote_upper)
            money_request = change_currency_data['money_request']
            
            if money_request<=0:
                return Response({'result': 'Money request couldn’t be 0'}, status=status.HTTP_200_OK)
            else:
                money_to_fulfill_request= calc_money_to_fulfill_request(money_request, base, quote)
                
                if money_to_fulfill_request[2]:
                    conversion_rate=money_to_fulfill_request[3]
                    track_fee = create_track_fee(money_request, base, quote)
                    serializer = Track_FeeSerializer(track_fee)
                    return Response(
                        {
                        'result': 'success',
                        'documentation': 'http://127.0.0.1:8000/swagger/',
                        'date_transaction':track_fee.date_transaction,
                        'money_request':track_fee.money_request,
                        'base_currency':track_fee.base_currency.name,
                        'base_new_quantity':track_fee.base_currency.quantity,                        
                        'quote_currency':track_fee.quote_currency.name,
                        'quote_new_quantity':track_fee.quote_currency.quantity,
                        'fee_amount':f'{track_fee.fee_amount} {track_fee.base_currency.name}',
                        'base_request':f'{track_fee.money_request} {track_fee.base_currency.name}',
                        'conversion_rate':f'{conversion_rate} {track_fee.quote_currency.name}'
                        
                        }, status=status.HTTP_200_OK)
                else:
                    return Response({'result': 'cant fulfill request'}, status=status.HTTP_200_OK)

                print(request.data)
                return Response({'result': 'we couldn’t found the currency'}, status=status.HTTP_404_NOT_FOUND)

class TrackFeeView(GenericAPIView):
    serializer_class = Track_Fee_GetFormatted_Serializer

    def get(self, request, id=None):
        track_fees = Track_Fee.objects.all()
        serializer = Track_FeeSerializer(track_fees, many=True)
        fees=[]
        for e in Track_Fee.objects.all():
            fee={
                "fee_amount": e.fee_amount,
                'money_request':e.money_request,
                "date_transaction": e.date_transaction,
                "base_currency": e.base_currency.name,
                "quote_currency": e.quote_currency.name
            }
            fees.append(fee)
        return Response({'result':'success', 'fees':fees})
 


def is_currency_exists(name):
    try:
        Currency.objects.get(name=name)
    except Currency.DoesNotExist:
        return False
    return True


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
            list_new_quantity = [new_base, new_quote, False]
            return list_new_quantity
        else:
            new_base.save()
            new_quote.save()

            list_new_quantity = [new_base, new_quote, True, quote_request]
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
        money_request=money_request_float_format,
        base_currency=base,
        quote_currency=quote
    )
    return tf

def generate_auto_currencies():

    EUR=Currency.objects.create(
                name='EUR',
                exchange=1.18,
                fee_percentage=0.01,
                quantity=1000
    )
    EUR.save()

    USD=Currency.objects.create(
                name='USD'.upper(),
                exchange=1,
                fee_percentage=0.0015,
                quantity=1000
            )
    USD.save()

    JPY=Currency.objects.create(
                name='JPY',
                exchange=0.0091,
                fee_percentage=0.0113,
                quantity=1000
    )
    JPY.save()

    GBP=Currency.objects.create(
                name='GBP',
                exchange=2.11,
                fee_percentage=0.0033,
                quantity=1000
    )
    GBP.save()

    CHF=Currency.objects.create(
                name='CHF',
                exchange=0.78,
                fee_percentage=0.0089,
                quantity=1000            )
    CHF.save()

    AUD=Currency.objects.create(
                name='AUD',
                exchange=0.73,
                fee_percentage=0.0015,
                quantity=1000
    )
    AUD.save()

    CAD=Currency.objects.create(
                name='CAD',
                exchange=0.78,
                fee_percentage=0.034,
                quantity=1000
    )
    CAD.save()

    NZD=Currency.objects.create(
        name='NZD',
                exchange=0.69,
                fee_percentage=0.0041,
                quantity=1000
            )
    NZD.save()