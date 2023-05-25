from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import ListView, DetailView, View
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F

from .models import User, Airport, Flight, Ticket, Seat
from .permissions import IsAdminUser
from .serializers import UserSerializer, FlightSerializer, TicketSerializer, AirportSerializer

from rest_framework import generics,viewsets,permissions,status
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import AllowAny,IsAuthenticated
import csv
import io
# Create your views here.

class UserRegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json=serializer.data
                json['token'] = token.key
                
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)
    
class UserLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username,password=password)
        
        if user:
            token,created = Token.objects.get_or_create(user=user)
            # login(request, user)
            return Response({'token': token.key}, status=200)
        return Response({'error': 'Wrong Credentials'}, status=400)
    
class UserLogoutView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            logout(request)
            return Response({'User logged out successfully'},status=200)
        else:
            raise NotAuthenticated("You are not logged in")

    
class UserDetailView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
class FlightViewSet(generics.ListAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['flight_number', 'departure_city', 'arrival_city', 'departure_time', 'arrival_time', 'price']


class FlightAdminViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [permissions.IsAdminUser]  # Only Admin can add, change or delete flights

    @action(detail=False, methods=['get'])
    def export_flights(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="flights.csv"'

        writer = csv.writer(response)
        writer.writerow(['Flight Number', 'Departure City', 'Arrival City', 'Departure Time', 'Arrival Time', 'Price', 'Capacity', 'Seats Remaining'])

        flights = Flight.objects.all()

        for flight in flights:
            writer.writerow([flight.flight_number, flight.departure_city, flight.arrival_city, flight.departure_time, flight.arrival_time, flight.price, flight.capacity, flight.seats_remaining])

        return response
    
    def update(self, request, *args, **kwargs):
        flight = self.get_object()
        response = super().update(request, *args, **kwargs)

        if flight.status == '3':
            Ticket.objects.filter(flight=flight).update(status='3')
            Seat.objects.filter(flight=flight).update(is_booked=False)

        return response
    
    
    
    @action(detail=False, methods=['get'])
    def get_pending_checkins(self, request):
        pending_tickets = Ticket.objects.filter(status='2')
        serializer = self.get_serializer(pending_tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# class FlightCreateAPIView(CreateAPIView):
#     permission_classes = [IsAdminUser]
#     queryset = Flight.objects.all()
#     serializer_class = FlightSerializer

#     def create(self, request, *args, **kwargs):
#         departure_airport, created = Airport.objects.get_or_create(name=request.data.get('departure_airport'))
#         arrival_airport, created = Airport.objects.get_or_create(name=request.data.get('arrival_airport'))

#         flight = Flight.objects.create(
#             flight_number=request.data.get('flight_number'),
#             departure_city=request.data.get('departure_city'),
#             departure_airport=departure_airport,
#             arrival_city=request.data.get('arrival_city'),
#             arrival_airport=arrival_airport,
#             departure_time=request.data.get('departure_time'),
#             arrival_time=request.data.get('arrival_time'),
#             price=request.data.get('price'),
#             capacity=request.data.get('capacity'),
#             status=request.data.get('status'),
#             seats_remaining=request.data.get('seats_remaining')
#         )

#         return Response(data=self.get_serializer(flight).data, status=status.HTTP_201_CREATED)

class BulkFlightUpload(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        csv_file = request.data['file']

        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)

        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            departure_airport, created = Airport.objects.get_or_create(name=column[2])
            arrival_airport, created = Airport.objects.get_or_create(name=column[4])

            _, created = Flight.objects.update_or_create(
                flight_number=column[0],
                departure_city=column[1],
                departure_airport=departure_airport,
                arrival_city=column[3],
                arrival_airport=arrival_airport,
                departure_time=column[5],
                arrival_time=column[6],
                price=column[7],
                capacity=column[8],
                status=column[9],
                seats_remaining=column[10]
            )

        return Response(status=status.HTTP_201_CREATED)


    
class TicketPurchaseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        flight_number = request.data.get('flight_number')
        seat_type = request.data.get('seat_type')
        if request.user.credits<=80:
            return Response({"detail": "Insufficient credit score."}, status=status.HTTP_403_FORBIDDEN)
        flight = Flight.objects.get(flight_number=flight_number)
        try:
            seat = Seat.objects.filter(flight=flight, type=seat_type, is_booked=False).order_by('seatnum').first()
            if not seat:
                return Response({'error': 'No seats of this type available'}, status=400)

            ticket = Ticket.objects.create(flight=flight, customer=request.user, price=seat.price, status='1', seat=seat.seatnum)
            ticket.save()

            seat.is_booked = True
            seat.save()

            return Response({'message': 'Ticket Purchased', 'seat_number': seat.seatnum}, status=200)
        except:
            return Response({'error': 'No seats available'}, status=400)
    
class CheckInRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        flight_number = request.data.get('flight_number')
        flight = Flight.objects.filter(flight_number=flight_number).first()
        if flight is None:
            return Response({"detail": "Flight not found."}, status=status.HTTP_400_BAD_REQUEST)

        ticket = Ticket.objects.filter(customer=request.user, flight=flight, status='1').first()

        if ticket is None:
            return Response({"detail": "Ticket not found."}, status=status.HTTP_400_BAD_REQUEST)

        ticket.status = '2'  # Update status to pending check-in
        ticket.save()

        return Response({"detail": "Check-in request submitted."}, status=status.HTTP_200_OK)



class CheckInView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        username = request.data.get('username')
        flight_number = request.data.get('flight_number')

        user = User.objects.filter(username=username).first()
        flight = Flight.objects.filter(flight_number=flight_number).first()

        if user is None or flight is None:
            return Response({"detail": "User or Flight not found."}, status=status.HTTP_400_BAD_REQUEST)

        ticket = Ticket.objects.filter(customer=user, flight=flight, status='2').first()

        if ticket is None:
            return Response({"detail": "Ticket not found."}, status=status.HTTP_400_BAD_REQUEST)


        ticket.status = '3'  # 更新状态为已值机
        ticket.save()
        user.credits+=10
        user.save()

        return Response({"detail": "Check-in successful."}, status=status.HTTP_200_OK)
    
class TicketRefundView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        flight_number = request.data.get('flight_number')

        flight = Flight.objects.filter(flight_number=flight_number).first()

        if flight is None:
            return Response({"detail": "Flight not found."}, status=status.HTTP_400_BAD_REQUEST)

        ticket = Ticket.objects.filter(customer=request.user, flight=flight, status='1').first()

        if ticket is None:
            return Response({"detail": "Ticket not found or already checked in."}, status=status.HTTP_400_BAD_REQUEST)

        ticket.status = '4'  # Update status to cancelled
        ticket.save()

        seat = Seat.objects.filter(flight=flight, seatnum=ticket.seat).first()
        seat.is_booked = False
        seat.save()

        request.user.credits -= 10  # Deduct credit score
        request.user.save()

        return Response({"detail": "Refund successful."}, status=status.HTTP_200_OK)


class AirportCreateAPIView(generics.CreateAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsAdminUser]

    
class HomeView(ListView):
    model = Flight
    template_name = 'home.html'