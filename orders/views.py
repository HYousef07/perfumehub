from decimal import Decimal

import stripe

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from cart.models import Cart, CartItem
from cart.views import _cart_id

from .forms import CheckoutForm
from .models import Order, OrderItem


@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        return redirect('cart:cart_detail')

    cart_items = CartItem.objects.filter(
        cart=cart,
        active=True
    ).select_related('perfume')

    if not cart_items.exists():
        return redirect('cart:cart_detail')

    total = sum(
        (item.sub_total() for item in cart_items),
        Decimal('0.00')
    )

    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                order = Order.objects.create(
                    customer=request.user,
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email'],
                    phone=form.cleaned_data['phone'],

                    billing_address=form.cleaned_data['billing_address'],
                    billing_city=form.cleaned_data['billing_city'],
                    billing_postcode=form.cleaned_data['billing_postcode'],
                    billing_country=form.cleaned_data['billing_country'],

                    shipping_address=form.cleaned_data['shipping_address'],
                    shipping_city=form.cleaned_data['shipping_city'],
                    shipping_postcode=form.cleaned_data['shipping_postcode'],
                    shipping_country=form.cleaned_data['shipping_country'],

                    total=total,
                    payment_status='pending'
                )

                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        perfume=cart_item.perfume,
                        perfume_name=cart_item.perfume.name,
                        quantity=cart_item.quantity,
                        price=cart_item.perfume.price
                    )

            # Create Stripe Checkout Session
            stripe.api_key = settings.STRIPE_SECRET_KEY

            line_items = []

            for item in order.items.all():
                line_items.append({
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': item.perfume_name,
                        },
                        'unit_amount': int(item.price * 100),
                    },
                    'quantity': item.quantity,
                })

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=(
                    request.build_absolute_uri(
                        reverse('orders:payment_success')
                    ) + '?session_id={CHECKOUT_SESSION_ID}'
                ),
                cancel_url=request.build_absolute_uri(
                    reverse('orders:checkout')
                ),
                client_reference_id=str(order.order_number),
                metadata={
                    'order_number': str(order.order_number),
                }
            )

            order.stripe_session_id = checkout_session.id
            order.save(update_fields=['stripe_session_id'])

            return redirect(checkout_session.url)

    else:
        form = CheckoutForm()

    return render(
        request,
        'orders/checkout.html',
        {
            'form': form,
            'cart_items': cart_items,
            'total': total,
        }
    )


@login_required
def payment_success(request):
    session_id = request.GET.get('session_id')

    if not session_id:
        return redirect('cart:cart_detail')

    stripe.api_key = settings.STRIPE_SECRET_KEY

    session = stripe.checkout.Session.retrieve(session_id)

    order = get_object_or_404(
        Order,
        stripe_session_id=session_id,
        customer=request.user
    )

    if session.payment_status == 'paid':
        order.payment_status = 'paid'
        order.save(update_fields=['payment_status'])

        # Empty the cart only after successful payment
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            CartItem.objects.filter(
                cart=cart,
                active=True
            ).delete()
        except Cart.DoesNotExist:
            pass

        return redirect(
            'orders:order_confirmation',
            order_number=order.order_number
        )

    return redirect('orders:checkout')


@login_required
def order_confirmation(request, order_number):
    order = get_object_or_404(
        Order,
        order_number=order_number,
        customer=request.user
    )

    return render(
        request,
        'orders/order_confirmation.html',
        {'order': order}
    )