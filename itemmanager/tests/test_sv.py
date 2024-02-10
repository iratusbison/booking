from django.test import TestCase, Client
from django.urls import reverse
from .models import Room, Booking
from datetime import datetime, timedelta

class BookingViewTests(TestCase):
    def setUp(self):
        # Create test data for rooms and bookings
        self.room = Room.objects.create(room_number='101')
        self.booking = Booking.objects.create(
            name='John Doe',
            address='123 Main St',
            phone='555-1234',
            aadhar='123456789012',
            price='100',
            checkin_datetime=datetime.now(),
            checkout_datetime=datetime.now() + timedelta(days=1)
        )
        self.booking.rooms.add(self.room)

    def test_room_list_view(self):
        # Test room list view
        response = self.client.get(reverse('room_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.room.room_number)

    def test_booking_detail_view(self):
        # Test booking detail view
        response = self.client.get(reverse('booking_detail', args=(self.booking.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')

    # Add more test cases for other views as needed...
