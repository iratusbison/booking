from django.contrib import admin
from itemmanager.models.expense import Expense
from itemmanager.models.aks import Room


admin.site.register(Room)
admin.site.register(Expense)
