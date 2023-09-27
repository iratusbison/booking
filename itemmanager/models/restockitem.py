from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from itemmanager.models.item import Item
from itemmanager.models.restock import Restock
from django.db.models import Sum, F, ExpressionWrapper, FloatField


class RestockItemManager(models.Manager):
    def filter_restock(self, restock):
        return super().get_queryset().filter(restock=restock)
    
    def filter_item(self, item):
        return super().get_queryset().filter(item=item)

    def restock_total_amount(self, *args, **kwargs):
        return super().get_queryset().filter(**kwargs).aggregate(models.Sum('restock_item_amount'))['restock_item_amount__sum'] or 0

    def restock_total_cost(self, *args, **kwargs):
        return super().get_queryset().filter(**kwargs).aggregate(models.Sum('restock_item_total_cost'))['restock_item_total_cost__sum'] or 0

class RestockItem(models.Model):
    restock = models.ForeignKey(Restock, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    restock_item_amount = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    restock_item_total_cost = models.FloatField()

    objects = RestockItemManager()

    class Meta:
        unique_together = (("restock", "item"))

    def __str__(self):
        return "%d %s(s) for %d" % (self.restock_item_amount, self.item.item_name, self.restock_item_total_cost)
    


   
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.item.stock_quantity = RestockItem.objects.filter(item=self.item).aggregate(models.Sum('restock_item_amount'))['restock_item_amount__sum'] or 0
        self.item.save()
    



