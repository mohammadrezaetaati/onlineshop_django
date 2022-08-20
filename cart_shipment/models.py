from django.db import models

from user.models import Customer, CustomerAddress
from store.models import Product,  SupplierProductDetail
# from payment.models import PaymentType,PaymentRecord


class DeliveryType(models.Model):
    name = models.CharField(max_length=50)
    fee = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete= models.CASCADE)
    generate_date_time = models.DateTimeField(auto_now_add=True)
    # peyment_type_id = models.ManyToManyField(PaymentType,through=PaymentRecord)
    delivery_type_id = models.ForeignKey(DeliveryType, on_delete=models.RESTRICT)
    delivery_address = models.ForeignKey(CustomerAddress, on_delete= models.RESTRICT)
    products_price = models.PositiveIntegerField(default=0)
    delivery_cost = models.PositiveIntegerField(default=0)
    discount = models.PositiveIntegerField(default=0)
    total_price = models.PositiveIntegerField(default=0)
    customer_note = models.CharField(max_length=500, null=True, blank=True)

    def save(self, *args, **kwargs): 
        self.total_price = self.products_price + self.delivery_cost - self.discount
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.customer} / {self.generate_date_time}'


class OrderItem(models.Model):
    order_id = models.ForeignKey(Order,on_delete=models.CASCADE)
    sup_pr_detail = models.ForeignKey(SupplierProductDetail, on_delete=models.RESTRICT)
    name = models.CharField(max_length=300)
    product_count = models.PositiveIntegerField(default=1)
    price_per_unit = models.PositiveIntegerField(default=0)
    item_price = models.PositiveIntegerField(default=0)
    supplier = models.CharField(max_length= 100)

    def __str__(self) -> str:
        return f'{self.order_id}/ {self.name}'

    def get_item_price(self):
        return self.product_count * self.price_per_unit


class DeliveryStatusCatalogue(models.Model):
    name = models.CharField(max_length= 100)

    def __str__(self) -> str:
        return self.name


class DeliveryStatus(models.Model):
    catalogue_id = models.ForeignKey(DeliveryStatusCatalogue,on_delete=models.RESTRICT)
    order_id = models.ForeignKey(Order,on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    notes = models.CharField(max_length= 255, null=True, blank= True)

    def __str__(self) -> str:
        return f'{self.order_id} / {self.catalogue_id}'


class Cart(models.Model):
    customer_id = models.OneToOneField(Customer,on_delete=models.CASCADE)
    last_update_date_time = models.DateTimeField(auto_now=True)
    sup_pr_detail_id = models.ManyToManyField(SupplierProductDetail,through='CartItem')
    delivery_type_id = models.ForeignKey(DeliveryType, on_delete=models.RESTRICT,null=True,blank=True)
    delivery_address_id = models.ForeignKey(CustomerAddress,on_delete=models.RESTRICT,null=True,blank=True)

    def __str__(self) -> str:
        return f'{self.customer_id.username} cart'

    def cart_products_price(self):
        amount = 0
        for item in self.cartitem_set.all():
            amount += item.get_item_price()
        return amount

    def cart_shippment_price(self):
        if self.delivery_type_id == None:
            return None
        elif self.cart_products_price() >= 500000:
            return 0
        else:
            return self.delivery_type_id.fee

    def cart_total_price(self):
        if self.delivery_address_id == None or self.delivery_type_id == None:
            return None
        return self.cart_products_price() + self.cart_shippment_price()


class CartItem(models.Model):
    sup_pr_detail_id = models.ForeignKey(SupplierProductDetail,on_delete=models.RESTRICT)
    product_count = models.PositiveIntegerField(default=0)
    cart_id = models.ForeignKey(Cart,on_delete=models.CASCADE)
    last_seen_unit_price = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.cart_id}/ {self.sup_pr_detail_id}'

    def get_item_price(self):
        return self.product_count * self.sup_pr_detail_id.price_per_unit