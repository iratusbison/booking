from django import template

register = template.Library()

@register.filter
def calculate_reduced_total(loan):
    total_amount = loan.amount + loan.calculate_interest()
    payments = loan.payment_set.all()  # Assuming the related name is "payment_set"

    for payment in payments:
        if payment.payment_type == 'installment':
            total_amount -= payment.amount

    return total_amount
