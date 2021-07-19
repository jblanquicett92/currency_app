from .models import Currency

class AutoGenerateCurrencies():
    
    is_first_time=True


    def generate(self):

        if is_first_time:

            is_first_time=False

            EUR=Currency.objects.create(
                name='EUR',
                exchange=1.18,
                fee_percentage=0.0015,
                quantity=1000
            )
            EUR.save()

            USD=Currency.objects.create(
                name='USD',
                exchange=1.18,
                fee_percentage=0.0015,
                quantity=1000
            )
            USD.save()

            JPY=Currency.objects.create(
                name='JPY',
                exchange=1.18,
                fee_percentage=0.0015,
                quantity=1000
            )
            JPY.save()

            GBP=Currency.objects.create(
                name='GBP',
                exchange=1.18,
                fee_percentage=0.0015,
                quantity=1000
            )
            GBP.save()

            CHF=Currency.objects.create(
                name='CHF',
                exchange=1.18,
                fee_percentage=0.0015,
                quantity=1000
            )
            CHF.save()

            AUD=Currency.objects.create(
                name='AUD',
                exchange=1.18,
                fee_percentage=0.0015,
                quantity=1000
            )
            AUD.save()

            CAD=Currency.objects.create(
                name='CAD',
                exchange=1.18,
                fee_percentage=0.0015,
                quantity=1000
            )
            CAD.save()

            NZD=Currency.objects.create(
                name='NZD',
                exchange=1.18,
                fee_percentage=0.0015,
                quantity=1000
            )
            NZD.save()