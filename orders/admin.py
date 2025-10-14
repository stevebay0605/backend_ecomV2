from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'price', 'quantity', 'get_cost']
    can_delete = False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'first_name', 'last_name', 'email', 'total_amount', 'status', 'created']
    list_filter = ['status', 'created']
    search_fields = ['order_number', 'email', 'first_name', 'last_name']
    readonly_fields = ['order_number', 'created', 'updated', 'user', 'email', 'first_name', 'last_name', 'phone', 'address', 'postal_code', 'city', 'total_amount', 'shipping_cost']
    inlines = [OrderItemInline]
    date_hierarchy = 'created'
    
    fieldsets = (
        ('Informations de commande', {
            'fields': ('order_number', 'status', 'created', 'updated')
        }),
        ('Informations client', {
            'fields': ('user', 'email', 'first_name', 'last_name', 'phone')
        }),
        ('Adresse de livraison', {
            'fields': ('address', 'postal_code', 'city')
        }),
        ('Montants', {
            'fields': ('total_amount', 'shipping_cost')
        }),
    )