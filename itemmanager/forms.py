from django import forms
from django.forms import formset_factory, inlineformset_factory
from django.forms.formsets import BaseFormSet
from django.utils.translation import gettext_lazy as _

from collections import defaultdict
from itemmanager.models.expense import Expense, ESection
from itemmanager.models.loan import Loan, Payment, Section
from itemmanager.models.invest import InPayment, Investment, InSection


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'amount', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class ESectionForm(forms.ModelForm):
    class Meta:
        model = ESection
        fields = ['name']


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['name']



class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_date', 'payment_type']
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
        }

class InSectionForm(forms.ModelForm):
    class Meta:
        model = InSection
        fields = ['name']



class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class InPaymentForm(forms.ModelForm):
    class Meta:
        model = InPayment
        fields = ['amount', 'payment_date', 'payment_type']
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
        }














