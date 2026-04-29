from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('add-to-cart/<int:burger_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/update/', views.update_cart_item, name='update_cart_item'),  
    path('cart/remove/', views.remove_cart_item, name='remove_cart_item'),  
    path('checkout/', views.checkout, name='checkout'),
    path('order-history/', views.order_history, name='order_history'),
    path('reviews/', views.reviews, name='reviews'),
    path('map/', views.map_view, name='map'),
    path('api/pickup-points/', views.get_pickup_points, name='get_pickup_points'),
]