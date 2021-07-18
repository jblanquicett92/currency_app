from django.urls import path
from . import views

urlpatterns = [

    path('v1/currencies/', views.CurrenciesView.as_view()),
    path('v1/currencies/<str:name>', views.CurrenciesView.as_view()),
    path('v1/check_exchange_rate/<str:base>/<str:quote>', views.Check_exchange_rate.as_view()),
    
]