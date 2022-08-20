from django.shortcuts import redirect, render
from django.db.models import Avg, Max, Min, Sum, F, Q
from django.views import View
from django.views.generic import ListView, FormView, DeleteView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from user.models import Customer

from .models import Product, SupplierProductItem, SupplierProductDetail, Comment
from .forms import CommentForm

# Create your views here.


class ProductList(ListView):
    model = Product
    template_name: str =  "store/products_list.html"
    # context_object_name = "products"
    paginate_by = 15

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.annotate(pr_min_price = Min('supplierproductitem__supplierproductdetail__price_per_unit',\
            filter=Q(supplierproductitem__supplierproductdetail__available_quantity__gt = 0)))
        q = self.request.GET.get("search")
        if q:
            qs = qs.filter(Q(name__icontains = q) | Q(description__icontains = q)).distinct()
        return qs


class ProductDetail(DetailView):
    model = Product
    template_name: str = "store/product_detail.html"
    context_object_name = "product"
    pk_url_kwarg = "id"

    def get_object(self):
        self.object = super().get_object(self.queryset)
        self.object.min_price =(SupplierProductDetail.objects\
            .filter(sup_pr_item_id__product=self.object,available_quantity__gt=0)\
            .aggregate(min_price= Min('price_per_unit')))['min_price']
        return self.object


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pr_items = SupplierProductDetail.objects\
            .filter(sup_pr_item_id__product=self.object,available_quantity__gt=0)
        context["pr_items"]  = pr_items
        if self.request.user.is_authenticated:
            customer = Customer.objects.get(user_ptr=self.request.user)
            comment_form = CommentForm(initial={'customer_id':customer.id, 'product_id' : self.object.id})
            context["comment_form"] = comment_form
        return context


@login_required
def add_comment(request):
    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form.cleaned_data['product_id'].rate_calculator()
            return redirect(reverse('product_detail', kwargs={'id': form.cleaned_data['product_id'].id, 'slug':form.cleaned_data['product_id'].slug}))
    return redirect ('/')


@login_required
def delete_comment(request, id):
    if request.method == "GET":
        comment = Comment.objects.get(id=id)
        product = comment.product_id
        comment.delete()
        product.rate_calculator()
        return redirect(reverse('product_detail', kwargs={'id': product.id, 'slug':product.slug}))


def like_comment(request, id):
    comment = Comment.objects.get(id=id)
    comment.like += 1
    comment.save()
    return redirect(reverse('product_detail', kwargs={'id': comment.product_id.id, 'slug':comment.product_id.slug}))

def dislike_comment(request, id):
    comment = Comment.objects.get(id=id)
    comment.dislike += 1
    comment.save()
    return redirect(reverse('product_detail', kwargs={'id': comment.product_id.id, 'slug':comment.product_id.slug}))


def test (request):
    print('***GET***',request.GET)
    print('***POST***',request.POST)