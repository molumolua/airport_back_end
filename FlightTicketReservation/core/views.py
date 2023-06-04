from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import ListView, DetailView, View
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F,Q


from .models import User, Airport, Flight, Ticket, Seat,Passenger,Order
from .permissions import IsAdminUser
from .serializers import UserSerializer, FlightSerializer, TicketSerializer, AirportSerializer, OrderSerializer, PassengerSerializer

from rest_framework import generics,viewsets,permissions,status
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import AllowAny,IsAuthenticated

from decimal import Decimal
import csv
import io
import random
from django.core.mail import send_mail
from django.core.mail import send_mail  # 发送邮件模块
from django.conf import settings    # setting.py添加的的配置信息

# 注册发送邮箱验证码
class SendEmailView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get("email")
        send_type=request.data.get("send_type")
        code = '%06d' % random.randint(0, 999999)
        send_status=-1
        if send_type == "register":
            email_title = "注册激活"
            email_body = "您的邮箱注册验证码为：{0}, 该验证码有效时间为两分钟，请及时进行验证。".format(code)
            # 发送邮件
            send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
            if not send_status:
                return False
        if send_type == "retrieve":
            email_title = "找回密码"
            email_body = "您的邮箱注册验证码为：{0}, 该验证码有效时间为两分钟，请及时进行验证。".format(code)
            # 发送邮件
            send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        if(send_status>0):
            return Response({'message': 'successful send','code':code}, status=200)
        else:
            return Response({'error': 'unsuccessful send','code':'error'}, status=400)


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
    
class OrderViewSet(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {'customer__username':['exact'],'flight__flight_number':['exact']}
    
class PassengerViewSet(generics.ListAPIView):
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {'id_card_number','full_name','email','phone_number'}

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def update(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().update(request, *args, **kwargs)
        else:
            # For non-admin users, allow only updates to 'food_option' field
            partial_data = {'food_option': request.data.get('food_option', None)}
            serializer = self.get_serializer(self.get_object(), data=partial_data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(self.get_object(), '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to the queryset, we need to forcibly invalidate the prefetch cache.
                self.get_object()._prefetched_objects_cache = {}

            return Response(serializer.data)

class FlightViewSet(generics.ListAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['flight_number', 'departure_city', 'arrival_city', 'departure_time', 'arrival_time', 'price']

    def get_queryset(self):
        queryset = Flight.objects.all()
        price_gte = self.request.query_params.get('price__gte', None)
        if price_gte is not None:
            price_gte = Decimal(price_gte)
            queryset = queryset.filter(price__gte=price_gte)

        price_lte = self.request.query_params.get('price__lte', None)
        if price_lte is not None:
            price_lte = Decimal(price_lte)
            queryset = queryset.filter(price__lte=price_lte)

        

        return queryset


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
        print("update")
        flight = self.get_object()
        response = super().update(request, *args, **kwargs)

        if flight.status == '3':
            Ticket.objects.filter(flight=flight).update(status='3')
            Seat.objects.filter(flight=flight).update(is_booked=False)

        return response
    
    @action(detail=False, methods=['put'], url_path='flight_number/(?P<flight_number>\w+)')
    def update_by_flight_number(self, request, flight_number=None):
        flight = Flight.objects.get(flight_number=flight_number)
        serializer = self.get_serializer(flight, data=request.data, partial=True)  # `partial=True` to make update partial
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if flight.status == '3':
            Ticket.objects.filter(flight=flight).update(status='3')
            Seat.objects.filter(flight=flight).update(is_booked=False)

        return Response(serializer.data)
    
    
    
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
            departure_airport, created = Airport.objects.get_or_create(IATA_code=column[2])
            arrival_airport, created = Airport.objects.get_or_create(IATA_code=column[4])

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
        n=request.data.get('count')
        if request.user.credits<=80:
                return Response({"detail": "Insufficient credit score."}, status=status.HTTP_403_FORBIDDEN)
        flight = Flight.objects.filter(flight_number=flight_number).exclude(status="3").first()
        if not flight:
            return Response({'error': 'Flight does not exist!'}, status=status.HTTP_404_NOT_FOUND)
        vis=[]
        tickets=[]
        seats=[]
        seatnums=[]
        all_price=0
        cnt=[0,0,0,0]
        tickets = request.data.get('order')
        for ticket in tickets:
            full_name=ticket.get('full_name')
            id_card_number=ticket.get('id_card_number')
            if not full_name:
                return Response({"error":"full name not provided"},status=status.HTTP_400_BAD_REQUEST)
            if not id_card_number:
                return Response({"error":"id not provided"},status=status.HTTP_400_BAD_REQUEST)
            
            if id_card_number in vis:
                return Response({'error': 'repeated people!'}, status=400)
            vis.append(id_card_number)
            seat_type = int(ticket.get('seat_type'))
            cnt[seat_type]+=1
            passenger=Passenger.objects.filter(id_card_number=id_card_number).first()
            tickets_history=Ticket.objects.filter(passenger=passenger,flight=flight).exclude(status='4').first()
            #如果买过票了
            if(tickets_history):
                return Response({'error': 'Passenger '+full_name+' have bought this flight!'}, status=400)
            #如果没有这个人，创建一个
            if(passenger is None ):
                passenger, created = Passenger.objects.update_or_create(
                    full_name=full_name,
                    id_card_number=id_card_number
                )

            cnt[seat_type]+=1
    
        for i in range(1,4):
            if(cnt[i] > len(Seat.objects.filter(flight=flight, type=seat_type, is_booked=False))):
                return Response({'error': 'No sufficient seats for type '+str(i)}, status=400)
        


        order = Order.objects.create(flight=flight, customer=request.user,price=0) 
        for ticket in tickets:
            full_name=ticket.get('full_name')
            id_card_number= ticket.get('id_card_number')
            seat_type = int(ticket.get('seat_type'))

            passenger=Passenger.objects.filter(id_card_number=id_card_number).first()

            try:
                seat = Seat.objects.filter(flight=flight, type=seat_type, is_booked=False).order_by('seatnum').first()
                print(seat.price)
                ticket = Ticket.objects.create(flight=flight, passenger=passenger, price=seat.price, status='1', seat=seat.seatnum)
                ticket.save()
                seat.is_booked=True
                seat.save()
                order.tickets.add(ticket)
                #tickets.append(ticket)
                all_price+=seat.price
                #seats.append(seat)
                seatnums.append(seat.seatnum)
                
            except:
                return Response({'error': 'No sufficient seats'}, status=400)
        
        order.price=all_price
        order.save()
        return Response({'message': 'Ticket Purchased', 'seat_numbers': seatnums}, status=200)
    
class CheckInRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        id_card_number = request.data.get('id_card_number')
        flight_number = request.data.get('flight_number')
        flight = Flight.objects.filter(flight_number=flight_number).first()
        passenger = Passenger.objects.filter(id_card_number =id_card_number ).first()
        if passenger is None or flight is None:
            return Response({"detail": "Passenger or Flight not found."}, status=status.HTTP_400_BAD_REQUEST)

        ticket = Ticket.objects.filter(passenger=passenger, flight=flight, status='1').first()

        if ticket is None:
            return Response({"detail": "Ticket not found."}, status=status.HTTP_400_BAD_REQUEST)

        ticket.status = '2'  # Update status to pending check-in
        ticket.save()

        return Response({"detail": "Check-in request submitted."}, status=status.HTTP_200_OK)



class CheckInView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        id_card_number = request.data.get('id_card_number')
        flight_number = request.data.get('flight_number')

        passenger = Passenger.objects.filter(id_card_number =id_card_number ).first()
        flight = Flight.objects.filter(flight_number=flight_number).first()

        if passenger is None or flight is None:
            return Response({"detail": "Passenger or Flight not found."}, status=status.HTTP_400_BAD_REQUEST)

        ticket = Ticket.objects.filter(passenger=passenger, flight=flight, status='2').first()

        if ticket is None:
            return Response({"detail": "Ticket not found."}, status=status.HTTP_400_BAD_REQUEST)


        ticket.status = '3'  # 更新状态为已值机
        ticket.save()
        
        request.user.credits+=10
        request.user.save()

        return Response({"detail": "Check-in successful."}, status=status.HTTP_200_OK)
    


class TicketRefundView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        id_card_number = request.data.get('id_card_number')
        flight_number = request.data.get('flight_number')

        passenger = Passenger.objects.filter(id_card_number =id_card_number ).first()
        flight = Flight.objects.filter(flight_number=flight_number).first()

        if passenger is None or flight is None:
            return Response({"detail": "Passenger or Flight not found."}, status=status.HTTP_400_BAD_REQUEST)

        ticket = Ticket.objects.filter(Q( status='1' ) | Q( status='2' ),passenger=passenger, flight=flight).first()

        if ticket is None:
            return Response({"detail": "Ticket not found."}, status=status.HTTP_400_BAD_REQUEST)

        ticket.status = '4'  # Update status to cancelled
        ticket.save()

        seat = Seat.objects.filter(flight=flight, seatnum=ticket.seat).first()
        seat.is_booked = False
        seat.save()

        request.user.credits -= 10  # Deduct credit score
        request.user.save()

        return Response({"detail": "Refund successful."}, status=status.HTTP_200_OK)

#新增get_city方法，返回所有城市
def get_city(request):
    cities = Airport.get_city()
    return JsonResponse({'cities': cities})

#新增get_airport方法，返回所有机场
def get_airport(request):
    cities = Airport.objects.values('city','city_name').distinct()

    city_airport_data = []

    for city in cities:
        city_airports = Airport.objects.filter(city=city['city'])
        city_airport_list = [{'value':airport.IATA_code,'label':airport.name} for airport in city_airports]

        city_data = {
            'value': city['city'],
            'label': city['city_name'],  
            'children': city_airport_list,
        }

        city_airport_data.append(city_data)

    return JsonResponse({'airports': city_airport_data})




class AirportCreateAPIView(generics.CreateAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsAdminUser]

    
class HomeView(ListView):
    model = Flight
    template_name = 'home.html'