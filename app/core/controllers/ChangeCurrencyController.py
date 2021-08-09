from rest_framework import status
from rest_framework.response import Response

from ..models import Currency
from ..test import TestCurrency
from .CurrencyController import CurrencyController


class ChangeCurrencyController:

    def exchange(request):
        

        change_currency_data = request.data
        base_upper = change_currency_data['base'].upper()
        quote_upper = change_currency_data['quote'].upper()

        # is_currency_exists regresa valor booleano en caso de que exista o no la moneda
        if CurrencyController.is_currency_exists(base_upper) and CurrencyController.is_currency_exists(quote_upper):
            base = Currency.objects.get(name=base_upper)
            quote = Currency.objects.get(name=quote_upper)
            money_request = change_currency_data['money_request']

            if money_request <= 0:
                return Response({'result': 'Money request couldn’t be 0'}, status=status.HTTP_200_OK)
            else:
                # calc_money_to_fulfill_request: método testeado para validar
                # si contamos con la capacidad de cambiar la divisa
                money_to_fulfill_request = TestCurrency.calc_money_to_fulfill_request(
                    money_request, base, quote)
                # calc_money_to_fulfill_request: regresa una lista
                # [0]Moneda Base
                # [1]Moneda Cotización
                # [2]True si podemos hacer el cambio o False si no
                # [3]Solicitud de dinero a moneda de cotización
                if money_to_fulfill_request[2]:
                    conversion_rate = money_to_fulfill_request[3]
                    track_fee = TestCurrency.create_track_fee(
                        money_request, base, quote)

                    return Response(
                        {
                            'result': 'success',
                            'documentation': 'http://127.0.0.1:8000/swagger/',
                            'date_transaction': track_fee.date_transaction,
                            'money_request': track_fee.money_request,
                            'base_currency': track_fee.base_currency.name,
                            'base_new_quantity': track_fee.base_currency.quantity,
                            'quote_currency': track_fee.quote_currency.name,
                            'quote_new_quantity': track_fee.quote_currency.quantity,
                            'fee_amount': f'{track_fee.fee_amount} {track_fee.base_currency.name}',
                            'base_request': f'{track_fee.money_request} {track_fee.base_currency.name}',
                            'conversion_rate': f'{conversion_rate} {track_fee.quote_currency.name}'

                        }, status=status.HTTP_200_OK)
                else:
                    return Response({'result': 'cant fulfill request'}, status=status.HTTP_200_OK)

        return Response({'result': 'we couldn’t found the currency'}, status=status.HTTP_404_NOT_FOUND)
