from django.contrib import admin
from .import models
import sqlite3
# Register your models here.
admin.site.register(models.vendor)
admin.site.register(models.unit)


class productAdmin(admin.ModelAdmin):
   # search_fields=['title','title__unit']
    list_display = ['title', 'unit']


admin.site.register(models.product, productAdmin)


class purchaseAdmin(admin.ModelAdmin):
   # search_fields=['product__title']
    list_display = ['id', 'product', 'quantity',
                    'price', 'total_amnt', 'vendor', 'purch_date']


admin.site.register(models.purchase, purchaseAdmin)


class saleAdmin(admin.ModelAdmin):
   # search_fields=['product__title']
    list_display = ['id', 'product', 'quantity',
                    'price', 'total_amnt', 'sale_date']


admin.site.register(models.sales, saleAdmin)


class InventoryAdmin(admin.ModelAdmin):
   # search_fields=['product__title','product__unit__title']
    list_display = ['product', 'purch_qty', 'sale_qty',
                    'total_bal_qty', 'purch_date', 'sale_date']


admin.site.register(models.inventory, InventoryAdmin)
