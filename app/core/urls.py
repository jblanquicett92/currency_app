from django.urls import path, include, re_path
from . import views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Backend Currency APP",
      default_version='v1',
      description="Public Documentation Backend Currency APP",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="jorgeabm1992@gmail.com"),
      license=openapi.License(name="MIT"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [

    re_path('v1/swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('v1/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('v1/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('v1/currencies/', views.CurrenciesView.as_view()),
    path('v1/currencies/<str:name>', views.CurrenciesView.as_view()),
    path('v1/check_exchange_rate/<str:base>/<str:quote>', views.Check_exchange_rate.as_view()),
    path('v1/change_currency/', views.Change_currency.as_view()),
    
]