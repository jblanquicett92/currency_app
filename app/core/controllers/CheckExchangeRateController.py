import datetime

from rest_framework import status
from rest_framework.response import Response

from ..models import Currency
from ..test import TestCurrency


class CheckExchangeRateController:

    def base_to_quote_details(request, base, quote):

        base_upper = base.upper()
        quote_upper = quote.upper()

        if base_upper:

            try:
                base_currency = Currency.objects.get(name=base_upper)
            except Currency.DoesNotExist:
                return Response({'result': 'we couldn’t find the currency'}, status=status.HTTP_404_NOT_FOUND)

        if quote_upper:

            try:
                quote_currency = Currency.objects.get(name=quote_upper)
            except Currency.DoesNotExist:
                return Response({'result': 'we couldn’t find the currency'}, status=status.HTTP_404_NOT_FOUND)

        fee_cost = TestCurrency.calc_ex_rate(base_currency, quote_currency)
        base_to_quote = TestCurrency.calc_base_to_quote(base_currency, quote_currency)

        return Response({
            'result': 'success',
            'documentation': "http://127.0.0.1:8000/swagger/",
            'current_time': datetime.datetime.now(),
            'base': base_upper,
            'quote': quote_upper,
            'conversion_rate': base_to_quote,
            'fee_cost': fee_cost,
        }, status=status.HTTP_200_OK)
