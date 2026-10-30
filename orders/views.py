
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

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

                    total=total
                )

                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        perfume=cart_item.perfume,
                        perfume_name=cart_item.perfume.name,
                        quantity=cart_item.quantity,
                        price=cart_item.perfume.price
                    )

                cart_items.delete()

            return redirect(
                'orders:order_confirmation',
                order_number=order.order_number
            )

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
