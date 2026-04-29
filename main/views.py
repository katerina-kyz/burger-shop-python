from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum
from .models import Burger, BurgerCategory, Order, OrderItem, Review, PickupPoint, BonusTransaction
from .forms import RegisterForm, ReviewForm
import json

def index(request):
    """Главная страница"""
    categories = BurgerCategory.objects.all()
    burgers = Burger.objects.filter(is_available=True)
    
    # Популярные бургеры (по количеству заказов)
    popular_burgers = Burger.objects.annotate(
        order_count=Sum('orderitem__quantity')
    ).order_by('-order_count')[:3]
    
    # Последние отзывы
    recent_reviews = Review.objects.filter(is_approved=True).order_by('-created_at')[:3]
    
    context = {
        'categories': categories,
        'burgers': burgers,
        'popular_burgers': popular_burgers,
        'recent_reviews': recent_reviews,
    }
    return render(request, 'main/index.html', context)

def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Начисляем приветственные бонусы
            user.bonus_points = 100
            user.save()
            BonusTransaction.objects.create(
                user=user,
                points=100,
                transaction_type='earn',
                description='Приветственные бонусы'
            )
            login(request, user)
            messages.success(request, 'Регистрация успешно завершена!')
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form})

def user_login(request):
    """Авторизация пользователя"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Добро пожаловать!')
            return redirect('index')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    return render(request, 'main/login.html')

def user_logout(request):
    """Выход из системы"""
    logout(request)
    return redirect('index')

@login_required
def add_to_cart(request, burger_id):
    """Добавление товара в корзину"""
    burger = get_object_or_404(Burger, id=burger_id)
    cart = request.session.get('cart', {})
    
    if str(burger_id) in cart:
        cart[str(burger_id)] += 1
    else:
        cart[str(burger_id)] = 1
    
    request.session['cart'] = cart
    messages.success(request, f'{burger.name} добавлен в корзину!')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'cart_count': sum(cart.values())})
    
    return redirect('index')

@login_required
def cart_view(request):
    """Просмотр корзины"""
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    
    for burger_id, quantity in cart.items():
        burger = Burger.objects.get(id=int(burger_id))
        subtotal = burger.price * quantity
        total += subtotal
        cart_items.append({
            'burger': burger,
            'quantity': quantity,
            'subtotal': subtotal
        })
    
    possible_bonuses = int(total / 10)
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'possible_bonuses': possible_bonuses,
    }
    return render(request, 'main/cart.html', context)

@login_required
def update_cart_item(request):
    """Обновление количества товара в корзине"""
    if request.method == 'POST':
        data = json.loads(request.body)
        burger_id = str(data.get('burger_id'))
        quantity = int(data.get('quantity'))
        
        cart = request.session.get('cart', {})
        
        if quantity <= 0:
            # Удаляем товар если количество 0 или меньше
            cart.pop(burger_id, None)
        else:
            cart[burger_id] = quantity
        
        request.session['cart'] = cart
        
        # Пересчитываем общую сумму
        total = 0
        for bid, qty in cart.items():
            burger = Burger.objects.get(id=int(bid))
            total += burger.price * qty
        
        return JsonResponse({
            'status': 'success',
            'cart_count': sum(cart.values()),
            'total': float(total)
        })
    
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def remove_cart_item(request):
    """Удаление товара из корзины"""
    if request.method == 'POST':
        data = json.loads(request.body)
        burger_id = str(data.get('burger_id'))
        
        cart = request.session.get('cart', {})
        
        if burger_id in cart:
            del cart[burger_id]
            request.session['cart'] = cart
        
        # Пересчитываем общую сумму
        total = 0
        for bid, qty in cart.items():
            burger = Burger.objects.get(id=int(bid))
            total += burger.price * qty
        
        return JsonResponse({
            'status': 'success',
            'cart_count': sum(cart.values()),
            'total': float(total)
        })
    
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def checkout(request):
    """Оформление заказа"""
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, 'Ваша корзина пуста')
        return redirect('cart')
    
    # Рассчитываем сумму заказа
    total = 0
    cart_items = []
    for burger_id, quantity in cart.items():
        burger = Burger.objects.get(id=int(burger_id))
        subtotal = burger.price * quantity
        total += subtotal
        cart_items.append({
            'burger': burger,
            'quantity': quantity,
            'subtotal': subtotal
        })
    
    # Параметры доставки
    FREE_DELIVERY_THRESHOLD = 1000
    DELIVERY_PRICE = 300
    
    if request.method == 'POST':
        delivery_method = request.POST.get('delivery_method')
        delivery_address = request.POST.get('delivery_address', '')
        pickup_point = request.POST.get('pickup_point', '')
        use_bonuses = int(request.POST.get('use_bonuses', 0))
        payment_method = request.POST.get('payment_method', 'cash')  # ДОБАВЛЕНО - способ оплаты
        
        # Расчёт стоимости доставки
        if delivery_method == 'pickup':
            delivery_cost = 0
        elif total >= FREE_DELIVERY_THRESHOLD:
            delivery_cost = 0
        else:
            delivery_cost = DELIVERY_PRICE
        
        # Проверяем использование бонусов
        if use_bonuses > request.user.bonus_points:
            use_bonuses = request.user.bonus_points
        
        # Ограничиваем использование бонусов суммой заказа
        if use_bonuses > total:
            use_bonuses = total
        
        final_total = total - use_bonuses + delivery_cost
        
        # Создаем заказ (ДОБАВЛЕНО payment_method)
        order = Order.objects.create(
            user=request.user,
            total_amount=final_total,
            delivery_address=delivery_address if delivery_method == 'delivery' else pickup_point,
            delivery_method=delivery_method,
            used_bonus_points=use_bonuses,
            earned_bonus_points=int(total / 10),
            delivery_cost=delivery_cost,
            payment_method=payment_method  # ДОБАВЛЕНО
        )
        
        # Создаем позиции заказа
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                burger=item['burger'],
                quantity=item['quantity'],
                price=item['burger'].price
            )
        
        # Списание бонусов
        if use_bonuses > 0:
            request.user.bonus_points -= use_bonuses
            BonusTransaction.objects.create(
                user=request.user,
                points=-use_bonuses,
                transaction_type='spend',
                description=f'Использовано при заказе #{order.id}'
            )
        
        # Начисление бонусов
        earned = int(total / 10)
        if earned > 0:
            request.user.bonus_points += earned
            BonusTransaction.objects.create(
                user=request.user,
                points=earned,
                transaction_type='earn',
                description=f'Начислено за заказ #{order.id}'
            )
        
        request.user.save()
        
        # Очищаем корзину
        request.session['cart'] = {}
        
        # Сообщение об успешном заказе (ОБНОВЛЕНО)
        if payment_method == 'online':
            messages.success(request, f'Заказ #{order.id} успешно оформлен! Оплата будет проведена на сайте.')
        else:
            messages.success(request, f'Заказ #{order.id} успешно оформлен! Оплата при получении.')
        
        return redirect('order_history')
    
    # GET запрос - показываем форму оформления
    pickup_points = PickupPoint.objects.all()
    possible_bonuses = int(total / 10)
    
    # Рассчитываем стоимость доставки для отображения
    if total >= FREE_DELIVERY_THRESHOLD:
        delivery_cost = 0
        delivery_message = f"Бесплатная доставка (при заказе от {FREE_DELIVERY_THRESHOLD} ₽)"
    else:
        delivery_cost = DELIVERY_PRICE
        delivery_message = f"Стоимость доставки: {DELIVERY_PRICE} ₽ (добавьте {FREE_DELIVERY_THRESHOLD - total} ₽ для бесплатной доставки)"
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'user_bonuses': request.user.bonus_points,
        'possible_bonuses': possible_bonuses,
        'pickup_points': pickup_points,
        'delivery_cost': delivery_cost,
        'delivery_message': delivery_message,
        'free_delivery_threshold': FREE_DELIVERY_THRESHOLD,
    }
    return render(request, 'main/checkout.html', context)

@login_required
def order_history(request):
    """История заказов пользователя"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'main/order_history.html', {'orders': orders})

def reviews(request):
    """Страница с отзывами (доступна всем, но оставлять могут только авторизованные)"""
    
    # Обработка POST запроса (добавление отзыва)
    if request.method == 'POST':
        # Проверяем, авторизован ли пользователь
        if not request.user.is_authenticated:
            messages.warning(request, 'Чтобы оставить отзыв, пожалуйста, войдите в систему')
            return redirect('login')
        
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, 'Спасибо за отзыв! Он будет опубликован после модерации.')
            return redirect('reviews')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
    else:
        form = ReviewForm()
    
    # Получаем все одобренные отзывы
    reviews_list = Review.objects.filter(is_approved=True).order_by('-created_at')
    burgers = Burger.objects.filter(is_available=True)
    
    context = {
        'form': form,
        'reviews': reviews_list,
        'burgers': burgers,
    }
    return render(request, 'main/reviews.html', context)

def map_view(request):
    """Страница с картой точек выдачи"""
    pickup_points = PickupPoint.objects.all()
    return render(request, 'main/map.html', {'pickup_points': pickup_points})

def get_pickup_points(request):
    """API для получения точек выдачи (для карты)"""
    points = PickupPoint.objects.all().values('id', 'name', 'address', 'latitude', 'longitude', 'working_hours', 'phone')
    return JsonResponse(list(points), safe=False)