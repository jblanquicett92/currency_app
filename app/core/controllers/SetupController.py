from rest_framework import status
from rest_framework.response import Response

from ..models import Currency


class SetupController:

    def generate_auto_currencies(request):
        generate_data = request.data

        try:
            generate=generate_data['generate']
        except Exception as e:
            print(e)
            return Response({'result': 'unexpected request'}, status=status.HTTP_400_BAD_REQUEST)
        
        if generate:
            SetupController._initialize_generate_currencies()
            return Response({'result': 'you have generated EUR, USD, JPY, GBP, CHF, AUD, CAD y NZD. currencies'}, status=status.HTTP_201_CREATED)
        return Response({'result': 'unexpected request'}, status=status.HTTP_400_BAD_REQUEST)
    
    def _initialize_generate_currencies():
        
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
