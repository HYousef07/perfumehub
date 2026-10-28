from .models import Cart, CartItem

def cart_item_count(request):
    count = 0
    if request.session.session_key:
        try:
            cart = Cart.objects.get(
                cart_id=request.session.session_key
            )
            cart_items = CartItem.objects.filter(
                cart=cart,
                active=True
            )
            count = sum(item.quantity for item in cart_items)
        except Cart.DoesNotExist:
            pass
    return {'cart_item_count': count}
