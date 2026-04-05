from .models import OrderItem

def cart_count(request):
    """Передаёт количество товаров в корзине во все шаблоны"""
    if request.user.is_authenticated:
        cart = request.session.get('cart', {})
        count = sum(cart.values())
        return {'cart_count': count}
    return {'cart_count': 0}

def user_bonuses(request):
    """Передаёт количество бонусов пользователя во все шаблоны"""
    if request.user.is_authenticated:
        return {'user_bonuses': request.user.bonus_points}
    return {'user_bonuses': 0}