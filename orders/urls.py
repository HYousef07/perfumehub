from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path(
        'confirmation/<uuid:order_number>/',
        views.order_confirmation,
        name='order_confirmation'
    ),
    path(
        'history/',
        views.order_history,
        name='order_history'
    ),
    path(
        'details/<uuid:order_number>/',
        views.order_details,
        name='order_details'
    ),
]