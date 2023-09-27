from django.db import models
from django.utils import timezone

class ItemManager(models.Manager):
    pass
    
class Item(models.Model):
    item_name = models.CharField(max_length=50, unique=True)
    item_price = models.FloatField()
    item_availability = models.BooleanField(default=True)
    item_image = models.ImageField(blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True, null=True)
    stock_quantity = models.PositiveIntegerField(default=0)


    objects = ItemManager()

    def __str__(self):
        return "%s | %d - %s" % (self.item_name, self.stock_quantity, 'Rp {0:,}'.format(self.item_price))

    @property
    def item_stock(self):
        from itemmanager.models.saleitem import SaleItem
        from itemmanager.models.restockitem import RestockItem
        sales = SaleItem.objects.sale_total_amount(item=self)
        restocks = RestockItem.objects.restock_total_amount(item=self)
        return restocks - sales

    @property
    def cost(self):
        from itemmanager.models.restockitem import RestockItem
        from itemmanager.models.restock import Restock

        restocks = RestockItem.objects.restock_total_amount(item=self)
        total_cost = RestockItem.objects.restock_total_cost(item=self)
        return total_cost / restocks
    
    def update_stock_quantity(self):
        from itemmanager.models.restockitem import RestockItem
        total_restock = RestockItem.objects.filter(item=self).aggregate(models.Sum('restock_item_amount'))['restock_item_amount__sum'] or 0
        self.stock_quantity = total_restock
        self.save()

    def total_revenue(self):
        from itemmanager.models.saleitem import SaleItem
        from itemmanager.models.restockitem import RestockItem
        total_sales = SaleItem.objects.sale_total_amount(item=self)
        total_restocks = RestockItem.objects.restock_total_amount(item=self)
        total_stock_reduced = total_restocks - total_sales
        revenue = total_stock_reduced * self.item_price
        return revenue
    
    



    