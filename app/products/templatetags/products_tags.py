from django import template
register = template.Library()
from products.models import PurchaseProducts
from products.models import SaleProducts


@register.filter
def currency_format(price):
    return "{:,.2f} ₺".format(price)

@register.simple_tag
def purchase_products_info(purchase, product):
    purchase_products = PurchaseProducts.objects.get(purchase=purchase, product=product)

    return purchase_products

@register.simple_tag
def sale_products_info(sale, product):
    sale_products = SaleProducts.objects.get(sale=sale, product=product)

    return sale_products