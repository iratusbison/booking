from django.urls import path
from django.contrib.auth import views as auth_views
from itemmanager.views.view_invest import  invest_list, investment_detail, add_investment, make_payment, delete_payment, isection_list, iadd_section
from itemmanager.views.view_expense import expense_list, add_expense, delete_expense, esection_list, add_esection
from itemmanager.views.view_loan import  loan_list, loan_detail, add_loan, make_payment, delete_payment, section_list, add_section, delete_section

urlpatterns = [
    #path('expense', expense_list, name='expense_list'),
    #path('add_expense/', add_expense, name='add_expense'),
    #path('delete_expense/<int:expense_id>/', delete_expense, name='delete_expense'),
    path('section/delete/<int:section_id>/', delete_section, name='delete_section'),
    path('section/list/', section_list, name='section_list'),
    path('section/add/', add_section, name='add_section'),
    path('section/delete/<int:section_id>/', delete_section, name='delete_section'),
    path('section/<int:section_id>/loan/list/', loan_list, name='loan_list'),
    path('section/<int:section_id>/loan/<int:loan_id>/', loan_detail, name='loan_detail'),
    path('section/<int:section_id>/loan/add/', add_loan, name='add_loan'),
    path('section/<int:section_id>/loan/<int:loan_id>/payment/', make_payment, name='make_payment'),
    path('section/<int:section_id>/loan/<int:loan_id>/delete_payment/', delete_payment, name='delete_payment'),
    path('isection/<int:isection_id>/invest/list/', invest_list, name='invest_list'),
    path('isection/<int:insection_id>/invest/<int:investment_id>/', investment_detail, name='investment_detail'),
    path('isection/<int:isection_id>/invest/add/', add_investment, name='add_investment'),
    path('isection/<int:isection_id>/invest/<int:investment_id>/payment/', make_payment, name='make_payment'),
    path('isection/<int:isection_id>/invest/<int:investment_id>/delete_payment/', delete_payment, name='delete_payment'),
    path('isection/list/', isection_list, name='isection_list'),
    path('isection/add/', iadd_section, name='iadd_section'),
    path('esection/', esection_list, name='esection_list'),
    path('esection/add/', add_esection, name='add_esection'),
    path('esection/<int:esection_id>/expenses/', expense_list, name='expense_list'),
    path('esection/<int:esection_id>/add_expense/', add_expense, name='add_expense'),
    path('esection/expense/<int:expense_id>/delete/', delete_expense, name='delete_expense'),

]
