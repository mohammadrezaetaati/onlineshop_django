from django.db import models
from django.urls import reverse

from User.models import Customer,Supplier

from django.core.validators import MaxValueValidator, MinValueValidator

from django.conf import settings



ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

class Product(models.Model):
    name=models.CharField(max_length=255 )
    price=models.IntegerField()
    quantity=models.IntegerField()
    supplier_name=models.ForeignKey(Supplier,on_delete=models.RESTRICT)
    category=models.ForeignKey("Category",on_delete=models.CASCADE)
    rate=models.FloatField(validators=[MaxValueValidator(5),MinValueValidator(1)])
    discount_id=models.ForeignKey("Discount",on_delete=models.CASCADE, null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    brand=models.ForeignKey("Brands",on_delete=models.DO_NOTHING,null=True,blank=True)
    img1=models.ImageField(upload_to=f'products/{name}')
    img2=models.ImageField(upload_to=f'products/{name}',null=True,blank=True)
    img3=models.ImageField(upload_to=f'products/{name}',null=True,blank=True)
    img4=models.ImageField(upload_to=f'products/{name}',null=True,blank=True)
    img5=models.ImageField(upload_to=f'products/{name}',null=True,blank=True)
    img6=models.ImageField(upload_to=f'products/{name}',null=True,blank=True)
    slug = models.SlugField(default='anonymous')
    feature = models.ManyToManyField("Feature", null=True, blank=True, through="ProductFeature")
    description = models.TextField(default='loremipson')


    def get_absolute_url(self):
        return reverse("productdetails", args=[str(self.id)])

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
            'slug': self.slug
        })

    # def get_remove_from_cart_url(self):
    #     return reverse("core:remove-from-cart", kwargs={
    #         'slug': self.slug
    #     })
    def __str__(self):
        return self.name


class ProductFeature(models.Model):
    feature = models.ForeignKey("Feature", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.product.name}-{self.feature.key}"


class Brands(models.Model):
    name=models.CharField(max_length=255)
    desc=models.TextField(null=True,blank=True)

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.item.name}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        # if self.item.discount_price:
        #     return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
        # payment = models.ForeignKey(
        # 'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    discount = models.ForeignKey(
        'Discount', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.discount:
            total -= self.discount.amount
        return total

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'
# class CartItem(models.Model):

#     count_order=models.IntegerField()
#     created_at=models.DateTimeField()
#     product_id=models.ForeignKey(Product ,on_delete=models.CASCADE)
#     session_id=models.ForeignKey("ShopSession", on_delete=models.CASCADE)
#     price=models.IntegerField()
#     ordered = models.BooleanField(default=False)
#     def get_total_item_price(self):
#         return self.quantity * self.item.price

#     def get_total_discount_item_price(self):
#         return self.quantity * self.item.discount_price

#     def get_amount_saved(self):
#         return self.get_total_item_price() - self.get_total_discount_item_price()

#     def get_final_price(self):
#         if self.item.discount_price:
#             return self.get_total_discount_item_price()
#         return self.get_total_item_price()

# class ShopSession(models.Model):
#     # customer_id=models.ForeignKey(Customer, on_delete=models.RESTRICT)
#     created_at=models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,
#                              on_delete=models.CASCADE)
#     ordered = models.BooleanField(default=False)



class Comment(models.Model):
    customer_id=models.ForeignKey(Customer,on_delete=models.RESTRICT)
    product_id=models.ForeignKey(Product, on_delete=models.CASCADE)
    comment_txt=models.TextField(blank=True,null=True)
    votes=models.IntegerField(null=True)
    created_at=models.DateTimeField(auto_now_add=True)

class Discount(models.Model):
    percent=models.FloatField()
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE, null=True, blank=True)
    desc=models.TextField(null=True)
    name=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
 

class Category(models.Model):
    title = models.CharField(max_length=200)
    feature_key = models.ManyToManyField("FeatureKey", null=True, blank=True)
    parent=models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.title


class FeatureKey(models.Model):
    name = models.CharField(max_length=255, null=True)


    def __str__(self):
        return self.name


class Feature(models.Model):
    feature_key = models.ForeignKey(FeatureKey, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.value
