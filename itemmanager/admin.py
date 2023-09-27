from django.contrib import admin
from itemmanager.models.item import Item
from itemmanager.models.restock import Restock
from itemmanager.models.sale import Sale

# Register your models here.
admin.site.register(Item)
admin.site.register(Restock)
admin.site.register(Sale)
#admin.site.register(StockNumber)