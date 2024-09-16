# Necessary imports
from django.db import models

# Create your models here.

class vendor(models.Model):
    full_name = models.CharField(max_length=50, default='Unknown Vendor')
    photo = models.ImageField(upload_to='vendor/', blank=True, null=True)
    address = models.TextField(default='No address provided')
    status = models.BooleanField(default=True)
    mobile = models.CharField(max_length=15, default='0000000000')

    class Meta:
        verbose_name_plural = 'vendors'

    def __str__(self):
        return self.full_name


class unit(models.Model):
    title = models.CharField(max_length=50, default='Default Unit')
    short_name = models.CharField(max_length=50, default='Default')

    class Meta:
        verbose_name_plural = 'units'

    def __str__(self):
        return self.title


class product(models.Model):
    title = models.CharField(max_length=50, default='Default Product')
    photo = models.ImageField(upload_to='product/', blank=True, null=True)
    detail = models.TextField(default='Default product details')
    unit = models.ForeignKey(unit, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'products'

    def __str__(self):
        return self.title


class purchase(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    vendor = models.ForeignKey(vendor, on_delete=models.CASCADE)
    quantity = models.FloatField()
    price = models.FloatField(default=10)
    total_amnt = models.FloatField(editable=False)
    purch_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'purchases'

    def save(self, *args, **kwargs):
        self.total_amnt = self.quantity * self.price
        super(purchase, self).save(*args, **kwargs)
        
        existing_inventory = inventory.objects.filter(product=self.product).order_by('id').first()
        if existing_inventory:
            totalbal = existing_inventory.total_bal_qty + self.quantity
        else:
            totalbal = self.quantity
                
        inventory.objects.create(
            product=self.product,
            purchase=self,
            sales=None,
            purch_qty=self.quantity,
            sale_qty=0,
            total_bal_qty=totalbal
        )


class sales(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.FloatField()
    price = models.FloatField(default=10)
    total_amnt = models.FloatField(editable=False)
    sale_date = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=50, blank=True)
    customer_mobile = models.CharField(max_length=50, blank=True)
    customer_address = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'sales'

    def save(self, *args, **kwargs):
        # Calculate total amount for the sale
        self.total_amnt = self.quantity * self.price
        # Save the sales object first
        super(sales, self).save(*args, **kwargs)

        # Get the existing inventory for the product
        existing_inventory = inventory.objects.filter(product=self.product).order_by('id').first()
        
        if existing_inventory:
            # Subtract the sale quantity from the current inventory balance
            totalbal = existing_inventory.total_bal_qty - self.quantity
        
            # Update the inventory with the sale
            inventory.objects.create(
                product=self.product,
                purchase=None,
                sales=self,
                purch_qty=None,
                sale_qty=self.quantity,
                total_bal_qty=totalbal  # Update the balance after the sale
            )




class inventory(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE, blank=True, null=True)
    purchase = models.ForeignKey(purchase, on_delete=models.CASCADE, blank=True, null=True)
    sales = models.ForeignKey(sales, on_delete=models.CASCADE, blank=True, null=True)
    purch_qty = models.FloatField(default=0, null=True)
    sale_qty = models.FloatField(default=0, null=True)
    total_bal_qty = models.FloatField(default=0, null=True)

    class Meta:
        verbose_name_plural = 'inventories'
    
    def purch_date(self):
        if self.purchase:
            return self.purchase.purch_date
    def sale_date(self):
        if self.sales:
            return self.sales.sale_date