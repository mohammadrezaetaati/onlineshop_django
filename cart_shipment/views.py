from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from django.contrib import messages
from django.db.models import Sum

from user.models import Customer, CustomerAddress
from store.models import SupplierProductDetail
from .models import Cart, CartItem, Order, OrderItem,\
    DeliveryStatus, DeliveryType



@login_required(login_url='/login')
def add_to_user_cart(request):
    origin_page = request.POST.get('origin_page')
    product_id = request.POST.get('product_id')
    product_slug = request.POST.get('product_slug')
    pr_det_id = request.POST.get('pr_det_id')
    product_count = int(request.POST.get('count'))

    customer = Customer.objects.get(user_ptr=request.user)
    cart = Cart.objects.get_or_create(customer_id=customer)[0]
    pr_det_item = SupplierProductDetail.objects.get(id=pr_det_id)
    cart_item = cart.cartitem_set.get_or_create(sup_pr_detail_id=pr_det_item)[0]
    if cart_item.product_count + product_count <= pr_det_item.available_quantity:
        cart_item.product_count += product_count
        messages.success(request, 'کالای موردنظر به تعداد خواسته شده به سبد خرید شما اضافه شد. جهت تایید نهایی و پرداخت لطفا وارد سبد خرید خود شوید')
    else:
        cart_item.product_count = pr_det_item.available_quantity
        messages.warning(request, 'حداکثر تعداد موجود از کالای موردنظر در سبد خرید شما اضافه شده است. جهت تایید نهایی و پرداخت لطفا وارد سبد خرید خود شوید')

    cart_item.save()

    return redirect(reverse(origin_page, kwargs={'id': product_id, 'slug': product_slug}))


@login_required(login_url='/login')
def remove_from_user_cart(request, id):

    cart_item = CartItem.objects.get(id=id)
    cart_item.delete()
    return redirect('show_cart')


@login_required(login_url='/login')
def edit_user_cart(request):
    for key in request.POST.keys():
        if (key != 'csrfmiddlewaretoken') and (key != 'origin_page'):
            cart_item = CartItem.objects.get(id=key)
            cart_item.product_count = request.POST.get(key)
            cart_item.save()
    return redirect('show_cart')
    

class ShowCart(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = CartItem
    template_name = "cart_shipment/show_cart.html"
    context_object_name = "cart_items"
    
    def get_queryset(self):
        query_set= super().get_queryset()
        customer = Customer.objects.get(user_ptr=self.request.user)
        query_set= query_set.filter(cart_id__customer_id=customer)
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = Customer.objects.get(user_ptr=self.request.user)
        customer_addresses = CustomerAddress.objects.filter(customer_id=customer)
        context['customer_addresses'] = customer_addresses
        delivery_types = DeliveryType.objects.all()
        context['delivery_types'] = delivery_types
        cart = Cart.objects.filter(customer_id=customer).first()
        context['cart'] = cart
        return context

    
@login_required(login_url='/login')
def set_shipping_address(request):
    delivery_address = request.POST.get('delivery_address')
    delivery_address = CustomerAddress.objects.get(id= delivery_address)
    delivery_type = request.POST.get('delivery_type')
    delivery_type = DeliveryType.objects.get(id= delivery_type)

    cart_id = request.POST.get('cart_id')
    cart = Cart.objects.get(id=cart_id)
    cart.delivery_type_id = delivery_type
    cart.delivery_address_id = delivery_address
    cart.save()
    return redirect('show_cart')


@login_required(login_url='/login')
def cart_checkout(request):
    
    customer = Customer.objects.get(user_ptr=request.user)
    cart: Cart = Cart.objects.get(customer_id=customer)
    
    flag = False
    for item in cart.cartitem_set.all():
        if item.product_count > item.sup_pr_detail_id.available_quantity:
            flag = True
            if item.sup_pr_detail_id.available_quantity == 0:
                item.delete()
            else:
                item.product_count = item.sup_pr_detail_id.available_quantity
                item.save()
    if flag:
        messages.error(request, 'با عرض پوزش، متاسفانه موجودی یک یا چند کالای انتخابی شما تغییر کرده است و اطلاعات سبد خرید به روز شده اند. لطفا مجددا سبد خرید خود را بررسی و تایید نمایید. (در صورتی که محصولی از سبد خربد شما حذف شده است، موجودی آن به اتمام رسیده است. لطفا در صورت تمایل مجددا به صفحه محصول مورد نظر مراجعه و آیتم دیگری را انتخاب نمایید)')
        return redirect('show_cart')

    order = Order(
        customer=customer,\
        delivery_type_id=cart.delivery_type_id,\
        delivery_address=cart.delivery_address_id,\
        products_price=cart.cart_products_price(),\
        delivery_cost=cart.cart_shippment_price()\
    )
    order.save()

    order.deliverystatus_set.create(catalogue_id_id=1)
    
    for item in cart.cartitem_set.all():
        
        sup_pr_detail = item.sup_pr_detail_id
        sup_pr_detail.available_quantity -= item.product_count
        sup_pr_detail.save()

        item_name = item.sup_pr_detail_id.sup_pr_item_id.product.name
        for elm in item.sup_pr_detail_id.productspecialfeature_set.all():
            item_name = item_name + f' {elm.spe_feature_key} : {elm.spe_feature_value}'
        
        order_item = OrderItem(
            order_id=order,
            sup_pr_detail=item.sup_pr_detail_id,
            name=item_name,
            product_count=item.product_count,
            price_per_unit=item.sup_pr_detail_id.price_per_unit,
            item_price= item.product_count * item.sup_pr_detail_id.price_per_unit,
            supplier=item.sup_pr_detail_id.sup_pr_item_id.supplier
        )
        order_item.save()

    cart.delete()
    
    # request.session['order_id'] = order.id
    # request.session['order_total_price'] = order.total_price
    # request.session['payment_type'] = 1   
    
    ### TODO: should be dynamic to make the customer able to choose different payment type
    return redirect(reverse('new_order_payment', kwargs={'order_id':order.id, 'payment_type_id':1}))


class ShowCustomerOrders(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Order
    template_name = "cart_shipment/show_customer_orders.html"
    context_object_name = "orders"
    
    def get_queryset(self):
        query_set= super().get_queryset()
        customer = Customer.objects.get(user_ptr=self.request.user)
        query_set= query_set.filter(customer=customer)\
            .order_by('-generate_date_time')\
            .annotate(total_products=Sum('orderitem__product_count'))
        list_number=1
        for item in query_set:
            item.last_state = item.deliverystatus_set.order_by('-date_time').first().catalogue_id
            item.num = list_number
            list_number +=1
        return query_set


class ShowOrderItems(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        order_last_state = order.deliverystatus_set.order_by('-date_time').first()
        payment_records = order.paymentrecord_set.order_by('-date_time')
        payment_records_detail = []
        for record in payment_records:

            date_time= record.date_time
            amount= record.paymentrecorddetail_set.filter(record_detail_key_id=2).first().record_detail_value
            card_no= record.paymentrecorddetail_set.filter(record_detail_key_id=5).first()
            if card_no:
                card_no= card_no.record_detail_value
            status= record.paymentrecorddetail_set.filter(record_detail_key_id=3).first().record_detail_value
            bank_track_id= record.paymentrecorddetail_set.filter(record_detail_key_id=8).first()
            if bank_track_id:
                bank_track_id= bank_track_id.record_detail_value

            payment_records_detail.append(
                {
                    "date_time" : date_time,
                    "amount" : amount,
                    "card_no" : card_no,
                    "status" : status,
                    "bank_track_id" : bank_track_id
                }
            )
        order_items = order.orderitem_set.all()
        context = {
            'order' : order,
            'order_last_state' : order_last_state,
            'payment_records' : payment_records_detail,
            'order_items' : order_items
        }
        
        return render(request, 'cart_shipment/show_order_items.html', context=context)


@login_required(login_url='/login')
def cancel_order(request, order_id):

    DeliveryStatus.objects.create(order_id_id=order_id, catalogue_id_id=6)
    order_items = OrderItem.objects.filter(order_id=order_id)
    for item in order_items:
        sup_pr_detail_item = SupplierProductDetail.objects.get(id=item.sup_pr_detail.id)
        sup_pr_detail_item.available_quantity += item.product_count
        sup_pr_detail_item.save()

    return redirect('show_customer_orders')