from django.urls import path

from .views import add_to_user_cart, remove_from_user_cart, edit_user_cart,\
    set_shipping_address, cart_checkout, cancel_order,\
    ShowCart, ShowCustomerOrders, ShowOrderItems
    

urlpatterns = [
    path('add-to-user-cart/', add_to_user_cart, name='add_to_user_cart'),
    path('edit-user-cart/', edit_user_cart, name='edit_user_cart'),
    path('remove-from-user-cart/<int:id>', remove_from_user_cart, name='remove_from_user_cart'),
    path('show-cart/', ShowCart.as_view(), name= 'show_cart'),
    path('set-shipping-address/', set_shipping_address, name='set_shipping_address'),    
    path('checkout/', cart_checkout, name='cart_checkout'),  
    path('show-customer-orders/', ShowCustomerOrders.as_view(), name= 'show_customer_orders'), 
    path('show-order-items/<int:order_id>', ShowOrderItems.as_view(), name= 'show_order_items'), 
    path('cancel_order/<int:order_id>', cancel_order, name='cancel_order'), 
]
