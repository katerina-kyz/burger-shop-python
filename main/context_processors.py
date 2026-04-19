from .models import Burger

def cart_count(request):
    """Передаёт количество товаров в корзине во все шаблоны"""
    if request.user.is_authenticated:
        cart = request.session.get('cart', {})
        count = sum(cart.values())
        return {'cart_count': count}
    return {'cart_count': 0}

def cart_total(request):
    """Передаёт сумму заказа в корзине во все шаблоны"""
    if request.user.is_authenticated:
        cart = request.session.get('cart', {})
        total = 0
        for burger_id, quantity in cart.items():
            try:
                from .models import Burger
                burger = Burger.objects.get(id=int(burger_id))
                total += burger.price * quantity
            except:
                pass
        return {'cart_total': total}
    return {'cart_total': 0}