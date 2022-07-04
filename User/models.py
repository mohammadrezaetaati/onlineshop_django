from logging import PlaceHolder
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.utils import timezone

TRANSACTION_STATUS = (
    ('Withdrawal', 'Withdrawal'),
    ('Credit', 'Credit'),
)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be provide')
        user = self.model(
            email=self.normalize_email(email), **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        if not email:
            raise ValueError('Email must be provide')
        superuser = self.model(
            email=self.normalize_email(email)
        )
        superuser.set_password(password)
        superuser.is_superuser = True
        superuser.is_staff = True
        superuser.save()
        return superuser


class User(AbstractBaseUser, PermissionsMixin):
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_suplier = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(
        max_length=11,
        validators=[RegexValidator(regex='^09\d{9}$', message='شماره تلفن را به درستی وارد کنید')], unique=True
    )
    email = models.EmailField(unique=True, )
    national_id = models.CharField(null=True, max_length=12, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    objects = UserManager()


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # class Meta:
    #     verbose_name = "Customer"


class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    shop_name = models.CharField(null=True, max_length=255)
    permission = models.BooleanField(default=False)
    supplier_rate = models.FloatField(null=True)
    supplier_rate_sum = models.IntegerField(default=0)


class AddressCustomer(models.Model):
    user = models.ForeignKey("Customer", on_delete=models.CASCADE)
    address = models.TextField()
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=10)


class WalletCustomer(models.Model):
    balance = models.PositiveIntegerField(default=0)
    customer = models.OneToOneField("Customer", on_delete=models.CASCADE)


class TransactionCustomer(models.Model):
    value = models.PositiveIntegerField()
    status = models.CharField(max_length=50, choices=TRANSACTION_STATUS, default='Withdrawal')
    wallet_id = models.ForeignKey("WalletCustomer", on_delete=models.RESTRICT)


class AddressSupplier(models.Model):
    user = models.ForeignKey("Supplier", on_delete=models.CASCADE)
    address = models.TextField()
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=10)


class WalletSupplier(models.Model):
    balance = models.PositiveIntegerField()
    supplier = models.OneToOneField("Supplier", on_delete=models.CASCADE)


class TransactionSupplier(models.Model):
    value = models.PositiveIntegerField()
    status = models.CharField(max_length=50, choices=TRANSACTION_STATUS, default='Withdrawal')
    wallet_id = models.ForeignKey("WalletSupplier", on_delete=models.RESTRICT)