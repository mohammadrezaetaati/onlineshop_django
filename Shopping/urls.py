from django.contrib import admin
from django.urls import path


from .views import ProductShow,Details,\
    cart_view,add_to_cart,remove_from_cart,\
    remove_single_item_from_cart,SearchProduct,FilterCategory,Comments

urlpatterns = [
    path('search-product', SearchProduct.as_view(),name='search-product'),
    path('comment', Comments.as_view(),name='comment'),
    path('productdetails/<int:id>', Details.as_view(),name='productdetails'),
    path('filter-category/<int:id>', FilterCategory.as_view(),name='filter-category'),
    path('cart/', cart_view ,name='cart'),
    path('add-to-cart/<int:id>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:id>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<int:id>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
]