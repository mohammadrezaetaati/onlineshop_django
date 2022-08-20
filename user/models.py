
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator


User = get_user_model()

class Customer(User):
    GENDER = [('M', 'مرد'), ('F', 'زن')]
    national_code = models.CharField(max_length=10, null=True, blank=True)
    phone_number = models.CharField(max_length= 10, validators=[RegexValidator(regex= r'^9\d{9}$', message='شماره تلفن وارد شده معتبر نمیباشد')])
    birthday = models.DateField(null=True, blank=True)
    job = models.CharField(max_length=255, null=True, blank=True)
    club_point = models.IntegerField(default=0)
    gender = models.CharField(max_length=1, choices=GENDER)
    education = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='users/customers/', default= 'default_user.png')

    class Meta:
        verbose_name = 'Customer'

    def __str__(self) -> str:
        return f'{self.username}'


class CustomerAddress(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    postal_address = models.TextField()
    postal_code = models.CharField(max_length=10)
    location_lat = models.FloatField(null=True, blank=True)
    location_lon = models.FloatField(null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.customer_id} / {self.postal_address} / {self.postal_code}'


class CustomerFavoriteCategory(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=100)


class NewsLetterSubscriber(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Supplier(User):
    phone_number = models.CharField(max_length= 10, validators= [RegexValidator(regex= r'^9\d{9}$', message='شماره تلفن وارد شده معتبر نمیباشد')])
    address = models.TextField()
    legal_information = models.JSONField(default=dict)
    clubs_point = models.IntegerField(default=0)
    image = models.ImageField(upload_to='users/suppliers/', default= 'default_user.png')

    class Meta:
        verbose_name = 'Supplier'

    def __str__(self) -> str:
        return f'{self.username}'


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Balance = models.FloatField(default=0)
    IBAN = models.CharField(max_length=24, null=True, blank=True)
    bank_card_number = models.CharField(max_length=16, null=True, blank=True)