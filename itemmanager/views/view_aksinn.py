import datetime
from django.shortcuts import render, redirect, get_object_or_404
from itemmanager.models.aks import Room, Booking

from datetime import datetime, timedelta

from django.db.models import Sum
from django.utils import timezone as djtimezone
from datetime import datetime, timedelta


from decimal import Decimal
from reportlab.lib.pagesizes import letter, A4
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet



from django.utils.timezone import make_aware

from django.contrib.auth.decorators import login_required
@login_required(login_url='/login')
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


@login_required(login_url='/login')
def room_list(request):
    rooms = Room.objects.all()
    now = djtimezone.now()
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
'''
@login_required(login_url='/login')
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
        other_charges = request.POST.get('other_charges')
        persons = request.POST.get('persons')
        reason = request.POST.get('reason')
        payment = request.POST.get('payment')


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
            other_charges=other_charges,
            email=email,
            persons=persons,
            reason=reason,
            payment=payment,
            checkin_datetime=checkin_datetime,
            checkout_datetime=checkout_datetime,
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
'''
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from itemmanager.models.aks import Room, Booking
from django.db import transaction

@login_required(login_url='/login')
#@transaction.atomic
def book_room(request):
    rooms = Room.objects.all()

    if request.method == 'POST':
        with transaction.atomic():
        # Process form submission
          room_ids = request.POST.getlist('rooms')  # Get selected room IDs from the form
          checkin_datetime = request.POST.get('checkin_datetime')
          checkout_datetime = request.POST.get('checkout_datetime')
          name = request.POST.get('name')
          address = request.POST.get('address')
          phone = request.POST.get('phone')
          email = request.POST.get('email')
          aadhar = request.POST.get('aadhar')
          price = request.POST.get('price')
          other_charges = request.POST.get('other_charges')
          persons = request.POST.get('persons')
          reason = request.POST.get('reason')
          payment = request.POST.get('payment')

        # Validate if the end date is not earlier than the start date
          if checkout_datetime <= checkin_datetime:
            error_message = 'Invalid date range'
            return render(request, 'book_room.html', {'rooms': rooms, 'error': error_message})

        # Perform additional validation if needed

        try:
            # Create the Booking object
            booking = Booking.objects.create(
                name=name,
                address=address,
                phone=phone,
                aadhar=aadhar,
                price=price,
                other_charges=other_charges,
                email=email,
                persons=persons,
                reason=reason,
                payment=payment,
                checkin_datetime=checkin_datetime,
                checkout_datetime=checkout_datetime,
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

        except ValueError:
            error_message = 'Invalid value for number. Please enter a valid number.'
            return render(request, 'book_room.html', {'rooms': rooms, 'error': error_message})

        except ValidationError as e:
            # Handle validation errors
            error_message = 'Validation error occurred. Please check your input.'
            return render(request, 'book_room.html', {'rooms': rooms, 'error': error_message})

    else:
        return render(request, 'book_room.html', {'rooms': rooms})

@login_required(login_url='/login')
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    rooms = booking.rooms.all()
    price = booking.price
    other_charges = booking.other_charges
    total_charges = Decimal(other_charges or 0) + price

    gst_amount = price - (price / (1 + Decimal('0.12')))
    net_price = price - gst_amount
    gst = price * Decimal('0.12')
    total_price = price + gst

    return render(request, 'booking_detail.html', {'booking': booking, 'rooms': rooms, 'price': price, 'gst': gst, 'gst_amount':gst_amount,'total_charges':total_charges, 'net_price':net_price,'total_price': total_price,'reason': booking.reason,})
@login_required(login_url='/login')
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
        booking.other_charges =request.POST.get('other_charges')

        booking.save()
        return redirect('booking_detail', booking_id=booking_id)
    else:
        return render(request, 'edit_booking.html', {'booking': booking,'rooms':rooms})

@login_required(login_url='/login')
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

from django.utils.timezone import make_aware

from decimal import Decimal
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO
from django.http import HttpResponse
from django.utils.timezone import make_aware, timezone

from decimal import Decimal
@login_required(login_url='/login')
def generate_pdf_book(request):
    # Check if a date range is provided in the request
    checkin_datetime = request.GET.get('checkin_datetime', '')
    checkout_datetime = request.GET.get('checkout_datetime', '')

    # Default to the last 30 days if no date range is provided
    if not checkin_datetime or not checkout_datetime:
        checkout_datetime = timezone.now()
        checkin_datetime = checkout_datetime - timedelta(days=30)
    else:
        checkin_datetime = make_aware(datetime.strptime(checkin_datetime, '%Y-%m-%d'))
        checkout_datetime = make_aware(datetime.strptime(checkout_datetime, '%Y-%m-%d'))

    # Filter bookings based on the provided date range
    bookings = Booking.objects.filter(checkin_datetime__range=(checkin_datetime, checkout_datetime))

    buffer = BytesIO()

    # Create PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]

    # Add title to the PDF with decoration
    title_text = f"Booking List ({checkin_datetime.date()} to {checkout_datetime.date()})"
    title = Paragraph(title_text, styles["Title"])
    title.alignment = 1  # Center alignment
    elements.append(title)
    '''
    # Add SV Mahal / AKS Inn to the top center
    elements.append(Paragraph("SV Mahal / AKS Inn", styles["Heading2"]))
    elements.append(Paragraph("No.192/1A 1B, Vandavasi Road, Sevilimedu, Kanchipuram - 631502", styles["BodyText"]))
    elements.append(Paragraph("Phone: 9842254415, 9443733265, 9994195966", styles["BodyText"]))
    elements.append(Paragraph("Email: svmahalaksinn@gmail.com", styles["BodyText"]))
    elements.append(Paragraph("GST: 33ADDFS68571Z8", styles["BodyText"]))
    elements.append(Paragraph("<br/><br/>", normal_style))  # Add space between address and table
    '''

    # Define data for the table
    data = [['ID', 'Name', 'Phone', 'Aadhar', 'Price', 'GST', 'Net Price']]

    total_revenue = Decimal('0.00')

    for booking in bookings:
        # Calculate GST and total price
        price = booking.price
        gst = price * Decimal('0.12')
        total_price = price + gst

        gst_amount = booking.price * Decimal('0.12')
        net_price = booking.price - gst_amount

        # Append booking details to the data list
        data.append([
            booking.id,
            booking.name,
            booking.phone,
            booking.aadhar,
            price,
            gst,
            net_price,
        ])

        # Increment total revenue
        total_revenue += price

    if len(data) == 1:
        data.append(['No bookings found', '', '', '', '', '', ''])  # If no bookings found, add a message row

    # Create the table
    table = Table(data)

    # Define style for the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    # Apply style to the table
    table.setStyle(style)
    elements.append(table)
    elements.append(Paragraph(f"Total Revenue: {total_revenue}", styles["Normal"]))

    # Build the PDF

    buffer.seek(0)
    # Build the PDF
    doc.build(elements)
    buffer.seek(0)

    # Create the HTTP response with PDF mime type
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="booking_list.pdf"'

    return response




from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from django.http import HttpResponse
from django.utils.timezone import localtime
from decimal import Decimal
from reportlab.lib.units import inch
@login_required(login_url='/login')
def generate_bill(request, booking_id):
    buffer = BytesIO()

    # Retrieve booking details
    booking = Booking.objects.get(id=booking_id)
    checkin_datetime_local = localtime(booking.checkin_datetime)
    checkout_datetime_local = localtime(booking.checkout_datetime)

    # Create a PDF document
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    title_style.alignment = 1  # Center alignment
    detail_style = styles["Normal"]

    # Content for the PDF
    content = []
    '''
    # Add SV Mahal/Aksinn Topic and Address, Email, Phone
    content.append(Paragraph("SV Mahal/Aksinn", title_style))
    content.append(Paragraph("No.192/1A 1B, Vandavasi Road, Sevilimedu, Kanchipuram - 631502", detail_style))
    content.append(Paragraph("Phone: 9842254415, 9443733265, 9994195966 ", detail_style))
    content.append(Paragraph("Email: svmahalaksinn@gmail.com", detail_style))
    content.append(Paragraph("GST: 33ADDFS68571Z8", detail_style))
    '''
    # Add title
    content.append(Paragraph("Booking Bill", title_style))
    total_charges = Decimal(booking.price or 0) + Decimal(booking.other_charges or 0)
    # Add booking details
    booking_details = [
        ["Booking ID:", str(booking.id)],
        ["Check-in Date:", str(checkin_datetime_local)],
        ["Check-out Date:", str(checkout_datetime_local)],
        ["Name:", booking.name],
        ['Address', "\n".join(booking.address.split(','))],
        ["Phone:", booking.phone],
        ["Aadhar:", booking.aadhar],
        ["Price:", str(booking.price)],
        ["other_charges:", str(booking.other_charges)],
        ["total_price:", total_charges],
        ["Email:", booking.email],
        ["Persons:", str(booking.persons)],
        ["Reason:", booking.reason],
        #['Rooms', ', '.join([room.room_number for room in booking.rooms.all()])],

    ]

    room_numbers = [room.room_number for room in booking.rooms.all()]
    room_lines = [", ".join(room_numbers[i:i+5]) for i in range(0, len(room_numbers), 5)]
    room_numbers_text = "\n".join(room_lines)

    booking_details.append(["Room Numbers:", room_numbers_text])

    # Add booking details to table
    booking_table = Table(booking_details, colWidths=[2*inch, 4*inch])
    booking_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 12),  # Increase font size
        ('TOPPADDING', (0, 0), (-1, -1), 8),  # Add padding to the cells
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))

    content.append(booking_table)

    # Calculate GST and net price
    gst_amount = booking.price * Decimal('0.12')
    net_price = booking.price - gst_amount

    # Add GST and net price to content
    content.append(Paragraph(f"GST (12%): {gst_amount}", detail_style))
    content.append(Paragraph(f"Net Price: {net_price}", detail_style))

    # Build the PDF
    doc.build(content)

    # Return the buffer content as HTTP response
    pdf = buffer.getvalue()
    buffer.close()

    # Create HTTP response with PDF content
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="booking_bill_{booking.id}.pdf"'
    return response


@login_required(login_url='/login')
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
@login_required(login_url='/login')
def room_check_list(request, room_id):
    # Retrieve the room object based on the room ID
    room = get_object_or_404(Room, id=room_id)

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

    # Retrieve bookings related to the room within the specified date range
    bookings = Booking.objects.filter(
        rooms=room,
        checkin_datetime__range=(checkin_datetime, checkout_datetime)
    )

    # Prepare a list to hold each booking along with its details
    bookings_with_details = []

    for booking in bookings:
        # Construct a dictionary with booking details
        booking_details = {
            'booking': booking,
            'checkin_datetime': booking.checkin_datetime,
            'checkout_datetime': booking.checkout_datetime,
        }

        bookings_with_details.append(booking_details)

    return render(request, 'room_check_list.html', {
        'room': room,
        'bookings': bookings_with_details,
        'checkin_datetime': checkin_datetime,
        'checkout_datetime': checkout_datetime,
    })
