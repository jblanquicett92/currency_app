

from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response


from .models import Track_Fee
from .serializers import (
    CurrencySerializer, Track_Fee_Formatted_Serializer, setup_Serializer)


from .controllers.CurrencyController import CurrencyController
from .controllers.SetupController import SetupController
from .controllers.CheckExchangeRateController import CheckExchangeRateController
from .controllers.ChangeCurrencyController import ChangeCurrencyController, CurrencyController


class SetupView(GenericAPIView):
    serializer_class = setup_Serializer

    def post(self, request, *args, **kwargs):
        return SetupController.generate_auto_currencies(request)


class CurrenciesView(GenericAPIView):
    serializer_class = CurrencySerializer

    def post(self, request, *args, **kwargs):
        return CurrencyController.create_new_currency(request)

    def get(self, request, name=None):
        return CurrencyController.list_or_read_currency(request, name)


class Check_exchange_rateView(GenericAPIView):

    def get(self, request, base, quote):

        return CheckExchangeRateController.base_to_quote_details(request, base, quote)


class Change_currencyView(APIView):
    serializer_class = Track_Fee_Formatted_Serializer

    def post(self, request):

        return ChangeCurrencyController.exchange(request)

# View encargada de listar todas las transacciones de cambios de divisas


class TrackFeeView(GenericAPIView):

    def get(self, request, id=None):
        track_fees = Track_Fee.objects.all()
        fees = []
        for e in Track_Fee.objects.all():
            fee = {
                "fee_amount": e.fee_amount,
                'money_request': e.money_request,
                "date_transaction": e.date_transaction,
                "base_currency": e.base_currency.name,
                "quote_currency": e.quote_currency.name
            }
            fees.append(fee)
        return Response({'status': 'success', 'fees': fees})
