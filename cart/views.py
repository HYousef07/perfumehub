
from django.shortcuts import get_object_or_404, redirect, render
from .models import Cart, CartItem
from perfumes.models import Perfume


def _cart_id(request):
    if not request.session.session_key:
        request.session.create()

    return request.session.session_key


def add_cart(request, perfume_id):
    perfume = get_object_or_404(Perfume, id=perfume_id)

    cart, created = Cart.objects.get_or_create(
        cart_id=_cart_id(request)
    )

    cart_item, created = CartItem.objects.get_or_create(
        perfume=perfume,
        cart=cart,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart:cart_detail')


def cart_detail(request):
    cart_items = []
    total = 0

    try:
        cart = Cart.objects.get(
            cart_id=_cart_id(request)
        )

        cart_items = CartItem.objects.filter(
            cart=cart,
            active=True
        )

        for cart_item in cart_items:
            total += cart_item.sub_total()

    except Cart.DoesNotExist:
        pass

    return render(
        request,
        'cart/cart.html',
        {
            'cart_items': cart_items,
            'total': total,
        }
    )