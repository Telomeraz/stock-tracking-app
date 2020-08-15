from django.db import models


class Persons(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True, verbose_name='Ad')
    active = models.BooleanField(default=True, verbose_name='Aktif')

    class Meta:
        verbose_name_plural = 'Kişiler'
        verbose_name = 'Kişi'

    def __str__(self):
        return self.name or 'İsimsiz'


class Products(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True, verbose_name='Ad')
    stock = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='Stok')
    stock_type = models.CharField(max_length=150, blank=True, null=True, verbose_name='Stok Tipi')
    active = models.BooleanField(default=True, verbose_name='Aktif')

    class Meta:
        verbose_name_plural = 'Ürünler'
        verbose_name = 'Ürün'

    def __str__(self):
        return self.name or 'İsimsiz'


class Purchases(models.Model):
    products = models.ManyToManyField(Products, through='PurchaseProducts')
    person = models.ForeignKey(Persons, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Satıcı')

    price_excluding_tax = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True, verbose_name='Vergi Hariç Alış Fiyatı')
    tax_amount = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True, verbose_name='Vergi Tutar')
    total_price = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True, verbose_name='Toplam Fiyat')

    purchase_date = models.DateField(blank=True, null=True, verbose_name='Alış Tarihi')

    class Meta:
        verbose_name_plural = 'Alışlar'
        verbose_name = 'Alış'
    
    def __str__(self):
        return str(self.person) + "'den Alış"

    def format_date(self):
        day = '0' + str(self.purchase_date.day) if self.purchase_date.day <= 9 else str(self.purchase_date.day)
        month = '0' + str(self.purchase_date.month) if self.purchase_date.month <= 9 else str(self.purchase_date.month)
        year = str(self.purchase_date.year)

        return day + '/' + month + '/' + year


class PurchaseProducts(models.Model):
    purchase = models.ForeignKey(Purchases, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Alış')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Ürün')

    unit_price = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True, verbose_name='Birim Alış Fiyatı')

    quantity = models.PositiveIntegerField(blank=True, null=True, verbose_name='Alış Adedi')

    class Meta:
        verbose_name_plural = 'Alış Ürünleri'
        verbose_name = 'Alış Ürünü'

    def __str__(self):
        return str(self.unit_price) or 'Fiyatsız'


class Sales(models.Model):
    products = models.ManyToManyField(Products, through='SaleProducts')
    person = models.ForeignKey(Persons, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Alıcı')

    price_excluding_tax = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True, verbose_name='Vergi Hariç Satış Fiyatı')
    tax_amount = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True, verbose_name='Vergi Tutar')
    total_price = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True, verbose_name='Toplam Fiyat')

    sale_date = models.DateField(blank=True, null=True, verbose_name='Satış Tarihi')

    class Meta:
        verbose_name_plural = 'Satışlar'
        verbose_name = 'Satış'

    def __str__(self):
        return str(self.person) + "'e Satış"

    def format_date(self):
        day = '0' + str(self.sale_date.day) if self.sale_date.day <= 9 else str(self.sale_date.day)
        month = '0' + str(self.sale_date.month) if self.sale_date.month <= 9 else str(self.sale_date.month)
        year = str(self.sale_date.year)

        return day + '/' + month + '/' + year


class SaleProducts(models.Model):
    sale = models.ForeignKey(Sales, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Satış')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Ürün')

    unit_price = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True, verbose_name='Birim Satış Fiyatı')

    quantity = models.PositiveIntegerField(blank=True, null=True, verbose_name='Satış Adedi')

    class Meta:
        verbose_name_plural = 'Satış Ürünleri'
        verbose_name = 'Satış Ürünü'

    def __str__(self):
        return str(self.unit_price) or 'Fiyatsız'