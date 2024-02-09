import datetime
from django.shortcuts import render, redirect, get_object_or_404
from itemmanager.models.aks import Room, Booking
from datetime import datetime, timedelta

from django.db.models import Sum


from decimal import Decimal
from reportlab.lib.pagesizes import letter, A4
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet

from django.utils import timezone

from django.utils.timezone import make_aware


def add_room(request):
    if request.method == 'POST':
        room_number = request.POST.get('room_number')


        # Create a new Room object and save it to the database
        Room.objects.create(
            room_number=room_number,

        )

        # Redirect to the room list page after adding the room
        return redirect('room_list')  # Assuming you have a URL named 'room_list'


    return render(request, 'room_add.html')



def room_list(request):
    rooms = Room.objects.all()
    now = timezone.now()
    for room in rooms:
        bookings = Booking.objects.filter(rooms=room, checkout_datetime__gte=now)
        if bookings.exists():
            room.is_available = False
            room.booking = bookings.first()
        else:
            room.is_available = True
            room.booking = None
    return render(request, 'room_list.html', {'rooms': rooms, 'now': now})




from django.core.exceptions import ValidationError
'''
def book_room(request):
    rooms = Room.objects.all()

    if request.method == 'POST':
        room_ids = request.POST.getlist('rooms')  # Get selected room IDs from the form
        checkin_datetime = request.POST.get('checkin_datetime')
        checkout_datetime = request.POST.get('checkout_datetime')
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        aadhar = request.POST.get('aadhar')
        price = request.POST.get('price')

        # Validate if the end date is not earlier than the start date
        if checkout_datetime <= checkin_datetime:
            error_message = 'Invalid date range'
            return render(request, 'book_room.html', {'rooms': rooms, 'error': error_message})

        # Initialize booking_id
        booking_id = None

        # Iterate through selected rooms and perform booking validation
        for room_id in room_ids:
            room = Room.objects.get(id=room_id)

            # Check if the room is already booked for the given date range
            existing_bookings = Booking.objects.filter(rooms=room, checkout_datetime__gte=checkin_datetime, checkin_datetime__lte=checkout_datetime)
            if existing_bookings.exists():
                error_message = f'Room {room.room_number} is already booked for the selected date range'
                return render(request, 'book_room.html', {'rooms': rooms, 'error': error_message})

            # Create a new booking for each selected room
            try:
                booking = Booking.objects.create(
                    name=name,
                    address=address,
                    phone=phone,
                    aadhar=aadhar,
                    price=price,
                    checkin_datetime=checkin_datetime,
                    checkout_datetime=checkout_datetime
                )
                booking.rooms.add(room)  # Add the room to the booking

                # Set the room's availability to False
                room.is_available = False
                room.save()

                # Assign the booking_id
                booking_id = booking.id

            except ValidationError as e:
                error_message = str(e)
                return render(request, 'book_room.html', {'rooms': rooms, 'error': error_message})

        # Redirect to booking_detail with the obtained booking_id
        return redirect('booking_detail', booking_id=booking_id)

    else:
        return render(request, 'book_room.html', {'rooms': rooms})
'''
from django.db import transaction

@transaction.atomic
def book_room(request):
    rooms = Room.objects.all()

    if request.method == 'POST':
        room_ids = request.POST.getlist('rooms')  # Get selected room IDs from the form
        checkin_datetime = request.POST.get('checkin_datetime')
        checkout_datetime = request.POST.get('checkout_datetime')
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        aadhar = request.POST.get('aadhar')
        price = request.POST.get('price')

        # Validate if the end date is not earlier than the start date
        if checkout_datetime <= checkin_datetime:
            error_message = 'Invalid date range'
            return render(request, 'book_room.html', {'rooms': rooms, 'error': error_message})

        # Create a new booking
        booking = Booking.objects.create(
            name=name,
            address=address,
            phone=phone,
            aadhar=aadhar,
            price=price,
            checkin_datetime=checkin_datetime,
            checkout_datetime=checkout_datetime
        )

        # Iterate through selected rooms and add them to the booking
        for room_id in room_ids:
            room = Room.objects.get(id=room_id)

            # Check if the room is already booked for the given date range
            existing_bookings = Booking.objects.filter(
                rooms=room,
                checkout_datetime__gte=checkin_datetime,
                checkin_datetime__lte=checkout_datetime
            )
            if existing_bookings.exists():
                error_message = f'Room {room.room_number} is already booked for the selected date range'
                booking.delete()  # Rollback the booking creation
                return render(request, 'book_room.html', {'rooms': rooms, 'error': error_message})

            # Add the room to the booking
            booking.rooms.add(room)

            # Set the room's availability to False
            room.is_available = False
            room.save()

        # Redirect to booking_detail with the obtained booking_id
        return redirect('booking_detail', booking_id=booking.id)

    else:
        return render(request, 'book_room.html', {'rooms': rooms})


def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    rooms = booking.rooms.all()
    price = booking.price
    gst = price * Decimal('0.12')
    total_price = price + gst

    return render(request, 'booking_detail.html', {'booking': booking, 'rooms': rooms, 'price': price, 'gst': gst, 'total_price': total_price})

def edit_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    rooms = booking.rooms.all()
    if request.method == 'POST':

        booking.checkin_datetime = request.POST.get('checkin_datetime')
        booking.checkout_datetime = request.POST.get('checkout_datetime')
        booking.name = request.POST.get('name')
        booking.address = request.POST.get('address')
        booking.phone = request.POST.get('phone')
        booking.aadhar = request.POST.get('aadhar')
        booking.email = request.POST.get('email')
        booking.price = request.POST.get('price')

        booking.save()
        return redirect('booking_detail', booking_id=booking_id)
    else:
        return render(request, 'edit_booking.html', {'booking': booking,'rooms':rooms})


def delete_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    rooms = booking.rooms.all()  # Get all rooms associated with the booking
    for room in rooms:
        room.is_available = True
        room.save()
    booking.delete()
    return redirect('room_list')


from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from io import BytesIO
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.timezone import make_aware

from decimal import Decimal

from reportlab.lib.styles import ParagraphStyle

def generate_pdf_book(bookings, checkin_datetime, checkout_datetime, total_revenue):
    buffer = BytesIO()

    # Create a PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Define styles
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
    name='Title',
    fontName='Helvetica-Bold',
    fontSize=16,
    alignment=1,  # Center alignment
    spaceAfter=20
      )

    detail_style = ParagraphStyle(
        name='Detail',
        fontName='Helvetica',
        fontSize=8,
        alignment=1
        )

    # Content for the PDF
    content = []

    # Add title
    content.append(Paragraph("SV Mahal / AKS Inn", title_style))

# Add details
    content.append(Paragraph("No.192/1A, Vandavasi Road, Sevilimedu, Kanchipuram - 631502", detail_style))
    content.append(Paragraph("Phone: 9842254415, 9994195966, 9443733265", detail_style))
    content.append(Paragraph("Email: ksaisandeep53@gmail.com", detail_style))
    content.append(Paragraph("GST: 33ADDFS68571Z8", detail_style))

    # Table header for booking details
    header = ['Booking ID', 'Price', 'GST (12%)', 'Total Price', 'Name',
              'Aadhar', 'Phone']

    # Prepare data for the PDF table
    booking_data = [header]
    for booking in bookings:
        # Calculate GST dynamically
        price = Decimal(booking.price)
        gst = price * Decimal('0.12')
        total_price = price + gst

        # Add booking details to the table
        room_names = [room.room_number for room in booking.rooms.all()]
        room_lines = [", ".join(room_names[i:i + 5]) for i in range(0, len(room_names), 5)]
        room_text = "\n".join(room_lines)

        row = [
            str(booking.id),

            str(booking.price),
            str(gst),
            str(total_price),
            booking.name,

            booking.aadhar,
            booking.phone,


        ]

        booking_data.append(row)

    # Create the PDF table
    booking_table = Table(booking_data)

    # Apply table styles
    booking_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Vertical alignment middle
    ]))

    content.append(booking_table)

    # Display total revenue
    content.append(Paragraph(f'Total Revenue: {total_revenue}', styles['Normal']))

    # Build the PDF document
    doc.build(content)

    # File is done, rewind the buffer.
    buffer.seek(0)
    return buffer

def download_pdf_bookings(request):
    # Get start and end dates from the request, defaulting to the last 30 days if not provided
    checkin_datetime_str = request.GET.get('checkin_datetime', '')
    checkout_datetime_str = request.GET.get('checkout_datetime', '')
    if not checkin_datetime_str or not checkout_datetime_str:
        checkout_datetime = datetime.now()
        checkin_datetime = checkout_datetime - timedelta(days=30)
    else:
        checkin_datetime = make_aware(datetime.strptime(checkin_datetime_str, '%Y-%m-%d'))
        checkout_datetime = make_aware(datetime.strptime(checkout_datetime_str, '%Y-%m-%d'))

    # Fetch bookings based on the date range
    bookings = Booking.objects.filter(checkin_datetime__range=(checkin_datetime,checkout_datetime))

    # Calculate total revenue for the given date range
    total_revenue = bookings.aggregate(Sum('price'))['price__sum']

    pdf_buffer = generate_pdf_book(bookings, checkin_datetime, checkout_datetime, total_revenue)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=bookings_list_{checkin_datetime_str}_{checkout_datetime_str}.pdf'
    response.write(pdf_buffer.read())

    return response

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from io import BytesIO
from decimal import Decimal
from django.utils import timezone

def generate_bill(request, booking_id):
    buffer = BytesIO()

    # Retrieve the booking object
    booking = Booking.objects.get(id=booking_id)
    checkin_datetime_local = timezone.localtime(booking.checkin_datetime)
    checkout_datetime_local = timezone.localtime(booking.checkout_datetime)
    # Create a PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Define styles
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        name='Title',
        fontName='Helvetica-Bold',
        fontSize=16,
        alignment=1,  # Center alignment
        spaceAfter=20
    )

    detail_style = ParagraphStyle(
        name='Detail',
        fontName='Helvetica',
        fontSize=8,
        alignment=1
    )

    # Content for the PDF
    content = []

    # Add title
    content.append(Paragraph("SV Mahal / AKS Inn", title_style))

    # Add details
    content.append(Paragraph("No.192/1A, Vandavasi Road, Sevilimedu, Kanchipuram - 631502", detail_style))
    content.append(Paragraph("Phone: 9842254415, 9994195966, 9443733265", detail_style))
    content.append(Paragraph("Email: ksaisandeep53@gmail.com", detail_style))
    content.append(Paragraph("GST: 33ADDFS68571Z8", detail_style))

    # Create data for the table
    data = [
        ["Booking ID", str(booking.id)],
        ['Rooms', ', '.join([room.room_number for room in booking.rooms.all()])],
        ["Name", booking.name],
        ['Address', "\n".join(booking.address.split(','))],  # Separate address by line breaks
        ["Phone", booking.phone],
        ["Aadhar", booking.aadhar],
        ["Price", str(booking.price)],
        ["GST", str(booking.price * Decimal('0.12'))],
        ["Total Price", str(booking.price * Decimal('1.12'))],
        ["Check-in Date", str(checkin_datetime_local)],
        ["Check-out Date", str(checkout_datetime_local)],
        ["Email", booking.email]  # Add email field
    ]



    # Separate room numbers into lines with a maximum of 5 numbers per line
    room_numbers = [room.room_number for room in booking.rooms.all()]
    room_lines = [", ".join(room_numbers[i:i+5]) for i in range(0, len(room_numbers), 5)]
    room_numbers_text = "\n".join(room_lines)

    data[1][1] = room_numbers_text

    table = Table(data)

    # Create the table
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Vertical alignment middle
        ]))

    content.append(table)


    # Build the PDF
    doc.build(content)

    # Return the buffer content as HTTP response
    pdf = buffer.getvalue()
    buffer.close()

    # Create HTTP response with PDF content
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="booking_bill_{booking.id}.pdf"'
    return response









def booking_list(request):
    # Check if a date range is provided in the request
    checkin_datetime = request.GET.get('checkin_datetime', '')
    checkout_datetime = request.GET.get('checkout_datetime', '')

    # Default to the last 30 days if no date range is provided
    if not checkin_datetime or not checkout_datetime:
        checkout_datetime = datetime.now()
        checkin_datetime = checkout_datetime - timedelta(days=30)
    else:
        checkin_datetime = make_aware(datetime.strptime(checkin_datetime, '%Y-%m-%d'))
        checkout_datetime = make_aware(datetime.strptime(checkout_datetime, '%Y-%m-%d'))

    bookings = Booking.objects.filter(checkin_datetime__range=(checkin_datetime, checkout_datetime))

    # Calculate total revenue for the given date range
    total_revenue = bookings.aggregate(Sum('price'))['price__sum']

    # Prepare a list to hold each booking along with its details
    bookings_with_details = []

    for booking in bookings:
        # Calculate GST for the booking
        price = float(booking.price)
        gst = price * 0.12

        # Collect room details for the booking
        room_details = ", ".join([room.room_number for room in booking.rooms.all()])

        # Construct a dictionary with booking details
        booking_details = {
            'booking': booking,
            'checkin_datetime': booking.checkin_datetime,
            'checkout_datetime': booking.checkout_datetime,
            'price': price,
            'gst': gst,
            'total_price': price + gst,
            'rooms': room_details,
        }

        bookings_with_details.append(booking_details)

    return render(request, 'booking_list.html', {
        'bookings': bookings_with_details,
        'checkin_datetime': checkin_datetime,
        'checkout_datetime': checkout_datetime,
        'total_revenue': total_revenue,

    })

'''
def booking_list(request):
    # Retrieve bookings
    bookings = Booking.objects.all()

    # Prepare a list to hold each booking along with its details
    bookings_with_details = []

    for booking in bookings:
        # Calculate GST for the booking
        price = float(booking.price)
        gst = price * 0.12

        # Collect room details for the booking
        room_details = ", ".join([room.room_number for room in booking.rooms.all()])

        # Construct a dictionary with booking details
        booking_details = {
            'booking': booking,
            'checkin_datetime': booking.checkin_datetime,
            'checkout_datetime': booking.checkout_datetime,
            'price': price,
            'gst': gst,
            'total_price': price + gst,
            'rooms': room_details,
        }

        bookings_with_details.append(booking_details)

    return render(request, 'booking_list.html', {'bookings': bookings_with_details})
'''
