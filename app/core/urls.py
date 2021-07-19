from django.urls import path, include, re_path
from . import views





urlpatterns = [


    path('v1/currencies/', views.CurrenciesView.as_view()),
    path('v1/currencies/<str:name>', views.CurrenciesView.as_view()),
    path('v1/check_exchange_rate/<str:base>/<str:quote>', views.Check_exchange_rateView.as_view()),
    path('v1/change_currency/', views.Change_currency.as_view()),
    path('v1/track_fee/', views.TrackFeeView.as_view()),
    path('v1/setup/', views.Setup.as_view()),
    
]