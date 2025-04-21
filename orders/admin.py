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
        'phone_number', 'mpesa_transaction_id', 'pickup_location', 'status'
    )
    list_editable = ('status',)
    list_filter = ('paid','status','created')
    inlines = [OrderItemInline]
    readonly_fields = ('created','updated')
