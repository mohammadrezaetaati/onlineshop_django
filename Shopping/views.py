
from itertools import product
from unicodedata import category
from django import views
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,JsonResponse
from django.views import View
from django.contrib import messages
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, View

from User.models import User,Customer

from .forms import SearchProductForm,CommentsForm
from .models import Category, Product,OrderItem,Order,Comment

class ProductShow(View):
    def get(self,request):
        products=Product.objects.all()
        categorys=Category.objects.all()
        context={
            'products':products,
            'categorys':categorys
            }
        return render(request,'index.html',context)


class Details(View):
    def get(self,request,id):
        product:Product=get_object_or_404(Product,id=id)
       
        # colors=product.feature.values_list('value')
        # print(product.feature.values_list())

        # photos:str=Product.objects.values_list('img1','img2','img3','img4','img5','img6')[1]

        context={
            'product':product,
            # 'colors':colors

            # 'photos':photos,
            }
        return render(request,'product-default.html',context)

class Comments(View):
    def post(self,request):
        form=CommentsForm(request.POST)
        if form.is_valid():
            comment=form.cleaned_data.get('comment')
            product=request.POST['product']
            votes=form.cleaned_data.get('rating')
            user=Customer.objects.get(user=request.user)
            print(product,'fffffffffffffffffffffffffff')
            Comment.objects.create(customer_id=user,product_id_id=product,comment_txt=comment,votes=votes)
            return render(reverse('project.views.detail', instance.id))
        # print(request.POST['comment'])
class SearchProduct(View):

    def post(self,request):
        form=SearchProductForm(request.POST)
        if form.is_valid():
            search=form.cleaned_data.get('search')
            products=Product.objects.filter(name__icontains=search)
            categorys=Category.objects.all()
            context={
                'products':products,
                'categorys':categorys
                }
            return render(request,'index.html',context)

class FilterCategory(View):

    def get(self,request,id):
        products=Product.objects.filter(category_id=id)
        categorys=Category.objects.all()
        context={
            'products':products,
            'categorys':categorys
            }
        return render(request,'index.html',context)

        
        

def cart_view(request):
    
    order = Order.objects.get(user=request.user, ordered=False)
    context = {
                'object': order
            }
   
       
    return render(request,'cart.html',context)


@login_required
def add_to_cart(request, id):
    item:Product = get_object_or_404(Product, id=id)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    print("2222")
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            print("1111")
            return redirect("cart")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("cart")
    else:
        print("3333")
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("cart")
 
def remove_from_cart(request, id):
    item = get_object_or_404(Product, id=id)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("cart")
    #     else:
    #         messages.info(request, "This item was not in your cart")
    #         return redirect("cart", id=id)
    # else:
    #     messages.info(request, "You do not have an active order")
    #     return redirect("cart", id=id)


@login_required
def remove_single_item_from_cart(request, id):
    item = get_object_or_404(Product, id=id)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("cart")
    #     else:
    #         messages.info(request, "This item was not in your cart")
    #         return redirect("core:product", id=id)
    # else:
    #     messages.info(request, "You do not have an active order")
    #     return redirect("core:product", id=id)
