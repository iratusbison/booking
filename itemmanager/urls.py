from django.urls import path
from django.contrib.auth import views as auth_views
from itemmanager.views.view_aksinn import add_room, room_list, book_room, edit_booking, delete_booking, generate_pdf_book, booking_detail, booking_list, generate_bill, download_pdf_bookings
from itemmanager.views.view_expense import expense_list, add_expense, delete_expense, esection_list, add_esection, generate_pdf
from itemmanager.views.view_invest import  invest_list, investment_detail, add_investment,  isection_list, iadd_section, rdsection_list, rd_list, rd_detail, Radd_section, add_rd
from itemmanager.views.view_income import income_list, add_income, delete_income, incsection_list, add_incsection, edit_income, monthly_income_list, add_monthly_income, edit_monthly_income, delete_monthly_income,generate_pdf_income
from itemmanager.views.view_todo import task_list, create_task, edit_task, delete_task
from itemmanager.views.view_total import total_view
from itemmanager.views.view_tax import calculate_tax
from itemmanager.views.view_chatgpt import query

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
    path('generate-pdf-income/<int:incsection_id>/', generate_pdf_income, name='generate_pdf_income'),


    path('task_list', task_list, name='task_list'),
    path('task/create/', create_task, name='create_task'),
    path('task/<int:pk>/edit/', edit_task, name='edit_task'),
    path('task/<int:pk>/delete/', delete_task, name='delete_task'),

    path('to/', total_view, name='another_view'),

    path('monthly_income/', monthly_income_list, name='monthly_income_list'),
    path('monthly_income/add/', add_monthly_income, name='add_monthly_income'),
    path('monthly_income/edit/<int:monthly_income_id>/', edit_monthly_income, name='edit_monthly_income'),
    path('monthly_income/delete/<int:monthly_income_id>/', delete_monthly_income, name='delete_monthly_income'),

    path('isection/<int:isection_id>/invest/list/', invest_list, name='invest_list'),
    path('isection/<int:insection_id>/invest/<int:investment_id>/', investment_detail, name='investment_detail'),
    path('isection/<int:isection_id>/invest/add/', add_investment, name='add_investment'),
    path('isection/list/', isection_list, name='isection_list'),
    path('isection/add/', iadd_section, name='iadd_section'),

    path('rdsection_list/', rdsection_list, name='rdsection_list'),
    path('rd_list/<int:rdsection_id>/', rd_list, name='rd_list'),
    path('rd_detail/<int:rdsection_id>/<int:rd_id>/', rd_detail, name='rd_detail'),
    path('Radd_section/', Radd_section, name='Radd_section'),
    path('add_rd/<int:rdsection_id>/', add_rd, name='add_rd'),

    path('calculate_tax/', calculate_tax, name='calculate_tax'),
    path('query/', query, name='query'),

    path('add/', add_room, name='add_room'),
    path('room_list', room_list, name='room_list'),
    path('book-room/', book_room, name='book_room'),
    path('edit-booking/<int:booking_id>/', edit_booking, name='edit_booking'),
    path('delete-booking/<int:booking_id>/', delete_booking, name='delete_booking'),
    path('generate-pdf/', generate_pdf_book, name='generate_pdf_book'),
    path('booking_detail/<int:booking_id>/', booking_detail, name='booking_detail'),
    path('booking_list/', booking_list, name='booking_list'),
    path('generate_bill/<int:booking_id>/', generate_bill, name='generate_bill'),
    path('download_pdf_bookings/', download_pdf_bookings, name='download_pdf_bookings'),



]
