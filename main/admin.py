from django.contrib import admin
from .models import CustomUser, BurgerCategory, Burger, Order, OrderItem, Review, PickupPoint, BonusTransaction

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'bonus_points', 'is_staff')
    search_fields = ('username', 'email', 'phone')
    list_filter = ('is_staff', 'is_active')

@admin.register(BurgerCategory)
class BurgerCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Burger)
class BurgerAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'calories', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'composition')
    list_editable = ('price', 'is_available')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'total_amount', 'status', 'delivery_method')
    list_filter = ('status', 'delivery_method', 'created_at')
    search_fields = ('user__username', 'delivery_address')
    list_editable = ('status',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'burger', 'quantity', 'price')
    search_fields = ('order__id', 'burger__name')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'burger', 'rating', 'created_at', 'is_approved')
    list_filter = ('rating', 'is_approved', 'created_at')
    list_editable = ('is_approved',)
    search_fields = ('user__username', 'comment')

@admin.register(PickupPoint)
class PickupPointAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'working_hours', 'phone')
    search_fields = ('name', 'address')
    list_editable = ('working_hours', 'phone')

@admin.register(BonusTransaction)
class BonusTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'transaction_type', 'description', 'created_at')
    list_filter = ('transaction_type', 'created_at')
    search_fields = ('user__username', 'description')