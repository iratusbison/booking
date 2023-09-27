from django import template



register = template.Library()

@register.filter
def total_revenue(saleitems):
    total = sum(item.sale_price for item in saleitems)
    return total
