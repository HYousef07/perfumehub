
import uuid

from django.conf import settings
from django.db import models
from perfumes.models import Perfume


class Order(models.Model):
    order_number = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='orders'
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    # Billing details
    billing_address = models.CharField(max_length=250)
    billing_city = models.CharField(max_length=100)
    billing_postcode = models.CharField(max_length=20)
    billing_country = models.CharField(max_length=100)

    # Shipping details
    shipping_address = models.CharField(max_length=250)
    shipping_city = models.CharField(max_length=100)
    shipping_postcode = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=100)

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.order_number)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    perfume = models.ForeignKey(
        Perfume,
        on_delete=models.SET_NULL,
        null=True
    )

    perfume_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def sub_total(self):
        return self.price * self.quantity

    def __str__(self):
        return f'{self.perfume_name} x {self.quantity}'
