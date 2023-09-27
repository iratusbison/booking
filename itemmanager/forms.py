from django import forms
from django.forms import formset_factory, inlineformset_factory
from django.forms.formsets import BaseFormSet
from django.utils.translation import gettext_lazy as _
from itemmanager.models.item import Item
from itemmanager.models.restock import *
from collections import defaultdict


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('item_name', 'item_price', 'item_image', 'description','stock_quantity' )


class SaleItemForm(forms.Form):
    quantity = forms.IntegerField(widget=forms.TextInput(
        attrs={'style': 'margin-bottom: 0', 'type': 'number'}))

    def __init__(self, *args, **kwargs):
        super(SaleItemForm, self).__init__(*args, **kwargs)
        items = Item.objects.all().order_by('item_name')
        item_choices = ()
        for item in items:
            item_choices = item_choices + ((item.pk, _(item.item_name)),)
        self.fields['item'] = forms.ChoiceField(
            choices=item_choices, label='', widget=forms.Select(attrs={'class': 'item-select'}))


class BaseSaleItemFormSet(BaseFormSet):
    def clean(self):
        """
        Adds validation, making sure total sales does not exceed item stock
        """
        if any(self.errors):
            return

        sales = defaultdict(int)

        errors = []
        for form in self.forms:
            if form.cleaned_data:
                item_pk = form.cleaned_data['item']
                quantity = form.cleaned_data['quantity']

                item = Item.objects.get(pk=item_pk)
                sales[item] += quantity

        for item, sale_amount in sales.items():
            print(item.item_stock, sale_amount)
            if sale_amount > item.stock_quantity:
                errors += [
                    forms.ValidationError(
                        _('Sale of %(item_name)s exceeds available stock'),
                        params={'item_name': item.item_name},
                        code='item_%d_stock_exceeded' % item.pk
                    )]

        if errors:
            raise forms.ValidationError(errors)


class RestockForm(forms.ModelForm):
    class Meta:
        model = Restock
        fields = ('restock_proof_of_payment', )

class RestockItemForm(forms.Form):
    quantity = forms.IntegerField(widget=forms.TextInput(
        attrs={'style': 'margin-bottom: 0', 'type': 'number'}))
    
    cost = forms.FloatField(widget=forms.TextInput(
        attrs={'style': 'margin-bottom: 0', 'type': 'number', 'step': '0.01'}))

    def __init__(self, *args, **kwargs):
        super(RestockItemForm, self).__init__(*args, **kwargs)
        items = Item.objects.all().order_by('item_name')
        item_choices = ()
        for item in items:
            item_choices = item_choices + ((item.pk, _(item.item_name)),)
        self.fields['item'] = forms.ChoiceField(
            choices=item_choices, label='', widget=forms.Select(attrs={'class': 'item-select'}))

class BaseRestockItemFormSet(BaseFormSet):
    pass