from rest_framework import status
from rest_framework.response import Response

from ..models import Currency
from ..serializers import CurrencySerializer


class CurrencyController:

    def create_new_currency(request):
        currency_data = request.data
        new_currency = Currency()
        try:
            name_upper = currency_data["name"].upper()
            if CurrencyController.is_currency_exists(name_upper):
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
            return Response({'result': 'success', 'new_currency': serializer.data}, status=status.HTTP_201_CREATED)

    def list_or_read_currency(request, name):
        if name:
            name_upper = name.upper()
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

    def is_currency_exists(name):
        try:
            Currency.objects.get(name=name)
        except Currency.DoesNotExist:
            return False
        return True
