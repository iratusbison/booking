from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from itemmanager.models.item import Item
from itemmanager.models.sale import Sale
from collections import defaultdict
from decimal import Decimal

class SaleItemManager(models.Manager):
    def sale_total_amount(self, item):
        return super().get_queryset().filter(item=item).aggregate(models.Sum('sale_amount'))['sale_amount__sum'] or 0
    
    def sale_total_revenue(self, sale):
        return super().get_queryset().filter(sale=sale).aggregate(models.Sum('sale_price'))['sale_price__sum'] or 0

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    sale_amount = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    sale_price = models.FloatField(blank=True, null=True, validators=[MinValueValidator(1)])

    objects = SaleItemManager()

    class Meta:
        unique_together = (("sale", "item"))

    def __str__(self):
        return "%s %s(s) for %d" % (self.item.item_name, self.sale_amount, self.sale_price)

    def clean(self):
        errors = {}
        if not self.item.item_availability:
            errors['item'] = ValidationError(
                _('Item not available!'), code='invalid')
        if self.sale_amount > self.item.item_stock:
            errors['sale_amount'] = ValidationError(
                _('Ensure sale amount is less or equal to item stock')
            )
        if errors:
            raise ValidationError(errors)
        
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.item.stock_quantity -= self.sale_amount
            self.item.save()
        super().save(*args, **kwargs)