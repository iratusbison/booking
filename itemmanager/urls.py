from django.urls import path
from django.contrib.auth import views as auth_views
from itemmanager.views.view_item import PricelistView , Item, ItemDeleteView, ItemDetailView, ItemEditView , ItemForm, ItemNewView, RestockItem
from itemmanager.views.view_restock import RestockListView, RestockDeleteView,RestockDetailView,RestockNewView
from itemmanager.views.view_sale import SaleListView, SaleNewView, SaleDetailView, SaleDeleteView ,SaleListViewWithTotal


urlpatterns = [
    path('pricelist/', PricelistView.as_view() , name='pricelist'),
    #path('items/new/', ItemNewView.as_view(), name='item_new'),
    path('items/<int:pk>/', ItemDetailView.as_view(), name='item_detail'),
    path('items/<int:pk>/edit', ItemEditView.as_view(), name='item_edit'),
    path('items/<int:pk>/delete', ItemDeleteView.as_view(), name='item_delete'),
    path('sales/', SaleListView.as_view(), name='sale_list'),
    path('sales/new/', SaleNewView.as_view(), name='sale_new'),
    path('sales/<int:pk>/', SaleDetailView.as_view(), name='sale_detail'),
    path('sales/<int:pk>/delete', SaleDeleteView.as_view(), name='sale_delete'),
    path('restocks/', RestockListView.as_view(), name='restock_list'),
    path('restocks/new/', RestockNewView.as_view(), name='restock_new'),
    path('restocks/<int:pk>/', RestockDetailView.as_view(), name='restock_detail'),
    path('restocks/<int:pk>/delete', RestockDeleteView.as_view(), name='restock_delete'),
     path('new_item/', ItemNewView.as_view(), name='new_item'),
    path('to', SaleListViewWithTotal.as_view(), name='sale_list_with_total'),
]