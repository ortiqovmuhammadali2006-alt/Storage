from django.urls import path 
from .views import home, product_by_category, product_detail, cart_view, category_detail, add_to_cart

urlpatterns = [
    path('', home, name='home'), 
    path('category/<slug:category_slug>/', product_by_category, name='category'), 
    path('product-detail/<slug:slug>/', product_detail, name='detail'),
    path('category-detail/<slug:slug>/', category_detail, name='category_detail'),
    path('cart/', cart_view, name='cart'),
    path('add-to-cart/<slug:product_slug>/', add_to_cart, name='add_to_cart'),
    
]
