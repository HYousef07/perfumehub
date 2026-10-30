
from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number',
        'customer',
        'first_name',
        'last_name',
        'email',
        'total',
        'created_at'
    )

    list_filter = (
        'created_at',
    )

    search_fields = (
        'order_number',
        'first_name',
        'last_name',
        'email',
        'customer__username',
    )

    ordering = ('-created_at',)

    date_hierarchy = 'created_at'

    readonly_fields = (
        'order_number',
        'created_at',
        'updated_at',
    )

    list_select_related = ('customer',)

    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'order',
        'perfume_name',
        'quantity',
        'price',
    )

    search_fields = (
        'perfume_name',
        'order__order_number',
    )
