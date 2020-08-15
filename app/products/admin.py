from django.contrib import admin

from products.models import *


class AdminPersons(admin.ModelAdmin):
    list_display = ('id', 'name', 'active')
    search_fields = ['name']
admin.site.register(Persons, AdminPersons)


class AdminProducts(admin.ModelAdmin):
    list_display = ('id', 'name', 'stock', 'active')
    search_fields = ['name']
admin.site.register(Products, AdminProducts)


class AdminPurchases(admin.ModelAdmin):
    list_display = ('id', 'person', 'price_excluding_tax', 'tax_amount', 'purchase_date')
    search_fields = ['person']

admin.site.register(Purchases, AdminPurchases)


class AdminPurchaseProducts(admin.ModelAdmin):
    list_display = ('id', 'purchase', 'product', 'unit_price', 'quantity')
    search_fields = ['purchase', 'product']
admin.site.register(PurchaseProducts, AdminPurchaseProducts)


class AdminSales(admin.ModelAdmin):
    list_display = ('id', 'person', 'price_excluding_tax', 'tax_amount', 'sale_date')
    search_fields = ['person']

admin.site.register(Sales, AdminSales)


class AdminSaleProducts(admin.ModelAdmin):
    list_display = ('id', 'sale', 'product', 'unit_price', 'quantity')
    search_fields = ['sale', 'product']
admin.site.register(SaleProducts, AdminSaleProducts)