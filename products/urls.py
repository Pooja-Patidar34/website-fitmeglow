# products/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail_view, name='product_detail'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist_view, name='add_to_wishlist'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('contact/', views.contact_us, name='contact_us'),
    path('add-selected-to-cart/', views.add_selected_to_cart_view, name='add_selected_to_cart'),
    path('add-all-to-cart/', views.add_all_to_cart_view, name='add_all_to_cart'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('update_cart_item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
     path('checkout/', views.checkout_view, name='checkout'),
    path('order/success/', views.order_success, name='order_success'),
]

