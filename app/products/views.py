from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from products.models import *


def calcBill(total_price):
    price_excluding_tax = total_price / 1.18
    tax_amount = total_price - price_excluding_tax

    price_excluding_tax = '{:.2f}'.format(price_excluding_tax)
    tax_amount = '{:.2f}'.format(tax_amount)
    total_price = '{:.2f}'.format(total_price)
    
    return price_excluding_tax, tax_amount, total_price


class PanelView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'panel/index_panel.html')


class PersonView(LoginRequiredMixin, View):
    def get(self, request):
        persons = Persons.objects.filter(active=True)

        context = {
            'persons': persons
        }

        return render(request, 'panel/persons/persons.html', context)


class AddPersonView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'panel/persons/add_person.html')
    
    def post(self, request):
        name = request.POST.get('name', '')
        
        person = Persons.objects.create(
            name=name
        )
        
        return redirect('/panel/kisiler/')


class EditPersonView(LoginRequiredMixin, View):
    def get(self, request, person_id):
        person = Persons.objects.get(id=person_id, active=True)

        context = {
            'person': person
        }

        return render(request, 'panel/persons/edit_person.html', context)
    
    def post(self, request, person_id):
        name = request.POST.get('name', '')
        
        person = Persons.objects.get(id=person_id, active=True)
        person.name = name
        person.save()
        
        return redirect('/panel/kisiler/')


class DeletePersonView(LoginRequiredMixin, View):
    def get(self, request, person_id):
        person = Persons.objects.get(id=person_id, active=True)

        person.active = False
        person.save()

        return redirect('/panel/kisiler/')


class ProductView(LoginRequiredMixin, View):
    def get(self, request):
        products = Products.objects.filter(active=True)

        context = {
            'products': products
        }

        return render(request, 'panel/products/products.html', context)


class AddProductView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'panel/products/add_product.html')
    
    def post(self, request):
        name = request.POST.get('name', '')
        stock = request.POST.get('stock', 0)
        stock_type = request.POST.get('stock_type', '')
        
        product = Products.objects.create(
            name=name,
            stock=stock,
            stock_type=stock_type
        )
        
        return redirect('/panel/urunler/')


class EditProductView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = Products.objects.get(id=product_id, active=True)

        context = {
            'product': product
        }

        return render(request, 'panel/products/edit_product.html', context)
    
    def post(self, request, product_id):
        name = request.POST.get('name', '')
        stock = request.POST.get('stock', 0)
        stock_type = request.POST.get('stock_type', '')
        
        product = Products.objects.get(id=product_id, active=True)
        product.name = name
        product.stock = stock
        product.stock_type = stock_type
        product.save()
        
        return redirect('/panel/urunler/')


class DeleteProductView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = Products.objects.get(id=product_id, active=True)

        product.active = False
        product.save()

        return redirect('/panel/urunler/')


class PurchaseView(LoginRequiredMixin, View):
    def get(self, request):
        purchases = Purchases.objects.prefetch_related('products').all()

        context = {
            'purchases': purchases
        }

        return render(request, 'panel/purchases/purchases.html', context)


class AddPurchaseView(LoginRequiredMixin, View):
    def get(self, request):
        persons = Persons.objects.filter(active=True)
        products = Products.objects.filter(active=True)

        context = {
            'persons': persons,
            'products': products
        }

        return render(request, 'panel/purchases/add_purchase.html', context)
    
    def post(self, request):
        person_id = request.POST.get('person', '')
        product_id = request.POST.getlist('product', '')
        unit_price = request.POST.getlist('unit_price', '')
        quantity = request.POST.getlist('quantity', '')
        date = request.POST.get('purchase_date', '')

        for i, item in enumerate(unit_price):
            unit_price[i] = item.replace(",", ".")

        date = date.split('/')
        purchase_date = ''
        for item in date[::-1]:
            purchase_date += '-' + item

        person = Persons.objects.get(id=person_id, active=True)

        purchase = Purchases.objects.create(
            person=person,
            purchase_date=purchase_date[1:]
        )

        total_price = 0

        for i, item in enumerate(product_id):
            total_price += float(unit_price[i]) * int(quantity[i])

            product = Products.objects.get(id=item, active=True)
            product.stock += int(quantity[i])
            product.save()

            PurchaseProducts.objects.create(
                purchase=purchase,
                product=product,
                unit_price=unit_price[i],
                quantity=quantity[i]
            )

        purchase.price_excluding_tax, purchase.tax_amount, purchase.total_price = calcBill(total_price)
        purchase.save()

        return redirect('/panel/alis-tablosu/')


class EditPurchaseView(LoginRequiredMixin, View):
    def get(self, request, purchase_id):
        purchase = Purchases.objects.get(id=purchase_id)
        purchase_products = PurchaseProducts.objects.filter(purchase=purchase)

        persons = Persons.objects.filter(active=True)
        products = Products.objects.filter(active=True)

        context = {
            'purchase': purchase,
            'purchase_products': purchase_products,
            'persons': persons,
            'products': products
        }

        return render(request, 'panel/purchases/edit_purchase.html', context)
    
    def post(self, request, purchase_id):
        person_id = request.POST.get('person', '')
        product_id = request.POST.getlist('product', '')
        unit_price = request.POST.getlist('unit_price', '')
        quantity = request.POST.getlist('quantity', '')
        date = request.POST.get('purchase_date', '')

        for i, item in enumerate(unit_price):
            unit_price[i] = item.replace(",", ".")

        date = date.split('/')
        purchase_date = ''
        for item in date[::-1]:
            purchase_date += '-' + item

        person = Persons.objects.get(id=person_id, active=True)
        
        purchase = Purchases.objects.get(id=purchase_id)
        purchase.person = person
        purchase.purchase_date = purchase_date[1:]

        purchase_products = PurchaseProducts.objects.filter(purchase=purchase)
        
        for item in purchase_products:
            if not item.product.stock < item.quantity:
                item.product.stock -= item.quantity
            else:
                item.product.stock = 0
            item.product.save()

        purchase_products.delete()

        total_price = 0

        for i, item in enumerate(product_id):
            total_price += float(unit_price[i]) * int(quantity[i])

            product = Products.objects.get(id=item, active=True)
            product.stock += int(quantity[i])
            product.save()

            PurchaseProducts.objects.create(
                purchase=purchase,
                product=product,
                unit_price=unit_price[i],
                quantity=quantity[i]
            )

        purchase.price_excluding_tax, purchase.tax_amount, purchase.total_price = calcBill(total_price)
        purchase.save()

        return redirect('/panel/alis-tablosu/')


class DeletePurchaseView(LoginRequiredMixin, View):
    def get(self, request, purchase_id):
        purchase = Purchases.objects.get(id=purchase_id)
        purchase.delete()

        return redirect('/panel/alis-tablosu/')


class SaleView(LoginRequiredMixin, View):
    def get(self, request):
        sales = Sales.objects.prefetch_related('products').all()

        context = {
            'sales': sales
        }

        return render(request, 'panel/sales/sales.html', context)


class AddSaleView(LoginRequiredMixin, View):
    def get(self, request):
        persons = Persons.objects.filter(active=True)
        products = Products.objects.filter(active=True)

        context = {
            'persons': persons,
            'products': products
        }

        return render(request, 'panel/sales/add_sale.html', context)
    
    def post(self, request):
        person_id = request.POST.get('person', '')
        product_id = request.POST.getlist('product', '')
        unit_price = request.POST.getlist('unit_price', '')
        quantity = request.POST.getlist('quantity', '')
        date = request.POST.get('sale_date', '')

        for i, item in enumerate(unit_price):
            unit_price[i] = item.replace(",", ".")

        date = date.split('/')
        sale_date = ''
        for item in date[::-1]:
            sale_date += '-' + item

        person = Persons.objects.get(id=person_id, active=True)

        sale = Sales.objects.create(
            person=person,
            sale_date=sale_date[1:]
        )

        total_price = 0

        for i, item in enumerate(product_id):
            total_price += float(unit_price[i]) * int(quantity[i])

            product = Products.objects.get(id=item, active=True)
            
            if not product.stock < int(quantity[i]):
                product.stock -= int(quantity[i])
            else:
                product.stock = 0
            product.save()

            SaleProducts.objects.create(
                sale=sale,
                product=product,
                unit_price=unit_price[i],
                quantity=quantity[i]
            )

        sale.price_excluding_tax, sale.tax_amount, sale.total_price = calcBill(total_price)
        sale.save()

        return redirect('/panel/satis-tablosu/')


class EditSaleView(LoginRequiredMixin, View):
    def get(self, request, sale_id):
        sale = Sales.objects.get(id=sale_id)
        sale_products = SaleProducts.objects.filter(sale=sale)

        persons = Persons.objects.filter(active=True)
        products = Products.objects.filter(active=True)

        context = {
            'sale': sale,
            'sale_products': sale_products,
            'persons': persons,
            'products': products
        }

        return render(request, 'panel/sales/edit_sale.html', context)
    
    def post(self, request, sale_id):
        person_id = request.POST.get('person', '')
        product_id = request.POST.getlist('product', '')
        unit_price = request.POST.getlist('unit_price', '')
        quantity = request.POST.getlist('quantity', '')
        date = request.POST.get('sale_date', '')

        for i, item in enumerate(unit_price):
            unit_price[i] = item.replace(",", ".")

        date = date.split('/')
        sale_date = ''
        for item in date[::-1]:
            sale_date += '-' + item

        person = Persons.objects.get(id=person_id, active=True)
        
        sale = Sales.objects.get(id=sale_id)
        sale.person = person
        sale.sale_date = sale_date[1:]

        sale_products = SaleProducts.objects.filter(sale=sale)
        
        for item in sale_products:
            item.product.stock += item.quantity
            item.product.save()

        sale_products.delete()

        total_price = 0

        for i, item in enumerate(product_id):
            total_price += float(unit_price[i]) * int(quantity[i])

            product = Products.objects.get(id=item, active=True)

            if not product.stock < int(quantity[i]):
                product.stock -= int(quantity[i])
            else:
                product.stock = 0
            product.save()

            SaleProducts.objects.create(
                sale=sale,
                product=product,
                unit_price=unit_price[i],
                quantity=quantity[i]
            )

        sale.price_excluding_tax, sale.tax_amount, sale.total_price = calcBill(total_price)
        sale.save()

        return redirect('/panel/satis-tablosu/')


class DeleteSaleView(LoginRequiredMixin, View):
    def get(self, request, sale_id):
        sale = Sales.objects.get(id=sale_id)
        sale.delete()

        return redirect('/panel/satis-tablosu/')
