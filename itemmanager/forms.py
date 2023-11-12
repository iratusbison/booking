from django import forms
from django.forms import formset_factory, inlineformset_factory
from django.forms.formsets import BaseFormSet
from django.utils.translation import gettext_lazy as _
from itemmanager.models.invest import  Investment, InSection, RD, RDSection
from collections import defaultdict
from itemmanager.models.expense import Expense, ESection

from itemmanager.models.income import Income,IncSection, MonthlyIncome
from itemmanager.models.todolist import Task

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['description', 'amount','status', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class IncSectionForm(forms.ModelForm):
    class Meta:
        model = IncSection
        fields = ['name']



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


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'start_date', 'due_date', 'completion', 'notes']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

class MonthlyIncomeForm(forms.ModelForm):
    class Meta:
        model = MonthlyIncome
        fields = ['description', 'amount', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
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

class RDSectionForm(forms.ModelForm):
    class Meta:
        model = RDSection
        fields = ['name']

class RDForm(forms.ModelForm):
    class Meta:
        model = RD
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }





class TaxCalculationForm(forms.Form):
    income = forms.DecimalField()
    deductions = forms.DecimalField(required=False)
    exemptions = forms.DecimalField(required=False)
