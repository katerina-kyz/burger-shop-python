from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, unique=True)
    bonus_points = models.IntegerField(default=0, verbose_name='Бонусные баллы')
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.username} - {self.bonus_points} баллов"

class BurgerCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Burger(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(BurgerCategory, on_delete=models.CASCADE, related_name='burgers')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    composition = models.TextField(help_text="Состав бургера")
    calories = models.IntegerField()
    image = models.ImageField(upload_to='burgers/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В обработке'),
        ('confirmed', 'Подтвержден'),
        ('preparing', 'Готовится'),
        ('ready', 'Готов к выдаче'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменен'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_address = models.TextField()
    pickup_point = models.CharField(max_length=200, blank=True, null=True)
    delivery_method = models.CharField(max_length=20, choices=[
        ('delivery', 'Доставка'),
        ('pickup', 'Самовывоз')
    ])
    used_bonus_points = models.IntegerField(default=0)
    earned_bonus_points = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    burger = models.ForeignKey(Burger, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def get_total(self):
        return self.price * self.quantity

class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews')
    burger = models.ForeignKey(Burger, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Review by {self.user.username} - {self.rating} stars"

class PickupPoint(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    working_hours = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name

class BonusTransaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bonus_transactions')
    points = models.IntegerField()
    transaction_type = models.CharField(max_length=20, choices=[
        ('earn', 'Начисление'),
        ('spend', 'Списание')
    ])
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.points} points - {self.transaction_type}"