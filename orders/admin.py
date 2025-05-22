from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product', 'price', 'quantity', 'size')
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'created', 'paid',
        'phone_number', 'benoti_phone_number', 'mpesa_transaction_id', 'benoti_transaction_id', 'pickup_location', 'status'
    )
    list_editable = ('status',)
    list_filter = ('paid', 'status', 'pickup_location', 'created')
    search_fields = ('id', 'user__username', 'phone_number', 'benoti_phone_number', 'mpesa_transaction_id', 'benoti_transaction_id', 'pickup_location')
    inlines = [OrderItemInline]
    readonly_fields = ('created', 'updated')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'get_cost')
    list_filter = ('order',)
    readonly_fields = ('get_cost',)
