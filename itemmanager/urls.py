from django.urls import path
from django.contrib.auth import views as auth_views

from itemmanager.views.view_expense import expense_list, add_expense, delete_expense, esection_list, add_esection, generate_pdf

from itemmanager.views.view_income import income_list, add_income, delete_income, incsection_list, add_incsection, edit_income
from itemmanager.views.view_todo import task_list, create_task, edit_task, delete_task
from itemmanager.views.view_total import total_view

urlpatterns = [
    #path('expense', expense_list, name='expense_list'),
    #path('add_expense/', add_expense, name='add_expense'),
    #path('delete_expense/<int:expense_id>/', delete_expense, name='delete_expense'),

    path('esection/', esection_list, name='esection_list'),
    path('esection/add/', add_esection, name='add_esection'),
    path('esection/<int:esection_id>/expenses/', expense_list, name='expense_list'),
    path('esection/<int:esection_id>/add_expense/', add_expense, name='add_expense'),
    path('esection/expense/<int:expense_id>/delete/', delete_expense, name='delete_expense'),
    path('generate-pdf/<int:esection_id>/', generate_pdf, name='generate_pdf'),

    path('incsection/', incsection_list, name='incsection_list'),
    path('incsection/add/', add_incsection, name='add_incsection'),
    path('incsection/<int:incsection_id>/incomes/', income_list, name='income_list'),
    path('incsection/<int:incsection_id>/add_income/', add_income, name='add_income'),
    path('incsection/income/<int:income_id>/delete/', delete_income, name='delete_income'),
    path('incsection/edit_income/<int:income_id>/', edit_income, name='edit_income'),


    path('task_list', task_list, name='task_list'),
    path('task/create/', create_task, name='create_task'),
    path('task/<int:pk>/edit/', edit_task, name='edit_task'),
    path('task/<int:pk>/delete/', delete_task, name='delete_task'),

    path('to/', total_view, name='another_view'),
]
