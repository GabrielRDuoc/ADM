from django.urls import path
from .views import *

urlpatterns = [
    path('venta_pasajes/<int:viaje_id>/', venta_pasajes, name='venta_pasajes'),
    path('confirmacion_venta/<int:ticket_id>/', confirmacion_venta, name='confirmacion_venta'),
    path('calendario_ofertas/', CalendarioOfertasView.as_view(), name='calendario_ofertas'),
    path('', login_view, name='login'),
    path('registro/', register_view, name='registro'),
   
]