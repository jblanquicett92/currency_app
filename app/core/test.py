from django.test import TestCase
from .models import Currency, Track_Fee
from django.db import transaction
import datetime

class CurrencyTestCase(TestCase):

    def setUp(self):

        Currency.objects.create(
            name='USD'.upper(),
            exchange=1,
            fee_percentage=0.0015,
            quantity=1000
        )
        Currency.objects.create(
            name='eur'.upper(),
            exchange=1.18,
            fee_percentage=0.01,
            quantity=1000
        )
        Currency.objects.create(
            name='gbp'.upper(),
            exchange=2.11,
            fee_percentage=0.0033,
            quantity=1000
        )
        Currency.objects.create(
            name='chf'.upper(),
            exchange=0.78,
            fee_percentage=0.0089,
            quantity=1000
        )
    
    #test validar que se guarda en mayusculas las divisas
    def test_upper_name(self):

       currency_A = Currency.objects.get(name='eur'.upper())
       currency_B = Currency.objects.get(name="chf".upper())

       self.assertEqual(currency_A.name, "EUR")
       self.assertEqual(currency_B.name, "CHF")
    

    #test para validar el porcentaje por transacción
    def test_exchange_rate(self):

        gbp = Currency.objects.get(name="GBP")
        eur = Currency.objects.get(name="EUR")

        chf = Currency.objects.get(name="CHF")
        usd = Currency.objects.get(name="USD")

        result_1=self.calc_ex_rate(gbp, eur)
        result_2=self.calc_ex_rate(chf, usd)      

        self.assertEqual(result_1, 0.028)
        self.assertEqual(result_2, 0.008)

    #test para validar el intercambio de divisas
    def test_base_to_quote(self):

        gbp = Currency.objects.get(name="GBP")
        eur = Currency.objects.get(name="EUR")

        chf = Currency.objects.get(name="CHF")
        usd = Currency.objects.get(name="USD")
        
        result_1=self.calc_base_to_quote(gbp, eur)
        result_2=self.calc_base_to_quote(chf, usd)
        result_3=self.calc_base_to_quote(gbp, chf)
        result_4=self.calc_base_to_quote(usd, eur)

        self.assertEqual(result_1, 1.788)
        self.assertEqual(result_2, 0.78)
        self.assertEqual(result_3, 2.705)
        self.assertEqual(result_4, 0.847)

    #Test para validar capacidad de intercambio de divisas
    def test_money_to_fulfill_request(self):
        
        request_1 = 80
        request_2 = 45
        request_3 = 435

        base = Currency.objects.get(name="gbp".upper())
        quote = Currency.objects.get(name="eur".upper())

        base_quote= self.calc_money_to_fulfill_request(request_1, base, quote)

        #caso 1, restando a diviza cotizada, para probar funcionamiento correcto
        self.assertEqual(base_quote[0].quantity, 1080)
        self.assertEqual(base_quote[1].quantity, 856.96)

        #caso 2, Se sigue restando a diviza cotizada, para probar funcionamiento correcto
        base_quote2= self.calc_money_to_fulfill_request(request_2, base, quote)
        self.assertEqual(base_quote2[0].quantity, 1125)
        self.assertEqual(base_quote2[1].quantity, 776.5)

        #caso 3, validacion de disponibilidad de dinero
        base_quote3= self.calc_money_to_fulfill_request(request_3, base, quote)
        self.assertEqual(base_quote2[0].quantity, 1125)
        self.assertEqual(base_quote2[1].quantity, 776.5)

    def test_crete_track_fee(self):
        request_1 = 40
        
        base = Currency.objects.get(name="gbp".upper())
        quote = Currency.objects.get(name="eur".upper())

        track_fee = self.create_track_fee(request_1, base, quote)
        self.assertEqual(track_fee.fee_amount, 2.3632)


    #valide con una prueba de unidad que la tarifa se está calculando correctamente.
    def calc_ex_rate(self, base_currency, quote_currency):

        fee = base_currency.fee_percentage+quote_currency.fee_percentage
        fee_cost = base_currency.exchange*fee
        formatted_float = "{:.3f}".format(fee_cost)
        return float(formatted_float)
    
    #
    def calc_base_to_quote(self, base_currency, quote_currency):
        base_to_quote = base_currency.exchange/quote_currency.exchange
        base_to_quote_float = "{:.3f}".format(base_to_quote)
        return float(base_to_quote_float)

    @transaction.atomic
    def calc_money_to_fulfill_request(self, money_request, base, quote):
        base_to_quote=self.calc_base_to_quote(base, quote)
        
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
    
    def create_track_fee(self, money_request, base, quote):

        money_request_float_format = float(money_request)
        print(money_request_float_format)

        fee_calc=self.calc_ex_rate(base, quote)
        fee_amount = base.exchange*money_request_float_format*fee_calc
        fee_amount_float_formatted = float("{:.4f}".format(fee_amount))

        tf = Track_Fee.objects.create(
            fee_amount=fee_amount_float_formatted,
            date_transaction=datetime.datetime.now(),
            base_currency=base,
            quote_currency=quote
        )
        return tf
