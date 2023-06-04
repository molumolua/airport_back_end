from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Flight, Ticket, Airport, Seat, Order, Passenger
from datetime import datetime
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        password = validated_data.pop('password', '')
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)
            print(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = '__all__'

class ShortAirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields=['name']

    def to_representation(self, instance):
        return instance.name.split(' ')[0]

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'


class FlightSerializer(serializers.ModelSerializer):
    departure_airport = ShortAirportSerializer()

    arrival_airport = ShortAirportSerializer()
    economy_seats_available = serializers.SerializerMethodField()
    business_seats_available = serializers.SerializerMethodField()
    first_class_seats_available = serializers.SerializerMethodField()
    departure_time = serializers.SerializerMethodField()
    arrival_time = serializers.SerializerMethodField()

    class Meta:
        model = Flight
        fields = '__all__'
        extra_kwargs = {
            'seats_remaining':{'required': False},
        }

    def get_departure_time(self, obj): 
        return obj.departure_time.strftime("%Y-%m-%d %H:%M") # convert to required format 
    def get_arrival_time(self, obj): 
        return obj.arrival_time.strftime("%Y-%m-%d %H:%M") # convert to required format 
    
    

    
    def get_economy_seats_available(self, obj):
        return Seat.objects.filter(flight=obj, type='3').filter(is_booked=False).count()

    def get_business_seats_available(self, obj):
        return Seat.objects.filter(flight=obj, type='2').filter(is_booked=False).count()

    def get_first_class_seats_available(self, obj):
        return Seat.objects.filter(flight=obj, type='1').filter(is_booked=False).count()
    
    def validate_departure_airport(self, value):
        try:
            Airport.objects.get(IATA_code=value)
        except Airport.DoesNotExist:
            raise serializers.ValidationError("Airport with this name does not exist.")
        return value

    def validate_arrival_airport(self, value):
        try:
            Airport.objects.get(IATA_code=value)
        except Airport.DoesNotExist:
            raise serializers.ValidationError("Airport with this name does not exist.")
        return value

    def create(self, validated_data):
        departure_airport_name = validated_data.pop('departure_airport')
        arrival_airport_name = validated_data.pop('arrival_airport')

        departure_airport = Airport.objects.get(IATA_code=departure_airport_name)
        arrival_airport = Airport.objects.get(IATA_code=arrival_airport_name)

        return Flight.objects.create(departure_airport=departure_airport, arrival_airport=arrival_airport, **validated_data)

    def update(self, instance, validated_data):
        departure_airport_name = validated_data.pop('departure_airport', None)
        arrival_airport_name = validated_data.pop('arrival_airport', None)
        departure_time = validated_data.pop('departure_time',None)

        if departure_airport_name is not None:
            instance.departure_airport = Airport.objects.get(IATA_code=departure_airport_name)
        if arrival_airport_name is not None:
            instance.arrival_airport = Airport.objects.get(IATA_code=arrival_airport_name)
        if departure_time is not None:
            instance.departure_time = datetime.strptime(departure_time, '%Y-%m-%d %H:%M') 
        
        return super().update(instance, validated_data)



class TicketSerializer(serializers.ModelSerializer):

    flight = serializers.SlugRelatedField(slug_field='flight_number', read_only=True)
    passenger = serializers.SlugRelatedField(slug_field='full_name', read_only=True)

    date_of_purchase = serializers.SerializerMethodField()

    def get_date_of_purchase(self, obj): 
        return obj.date_of_purchase.strftime("%Y-%m-%d %H:%M") # convert to required format 

    class Meta:
        model = Ticket
        fields = '__all__'

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'

class PassengerSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    seat = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only = True)
    ticketid = serializers.IntegerField(read_only = True)
    class Meta:
        model = Passenger
        fields = ['id_card_number','full_name','email','phone_number','seat','status','ticketid']

class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True)
    customer = serializers.SlugRelatedField(slug_field='username', read_only=True)
    flight = serializers.SlugRelatedField(slug_field='flight_number', read_only=True)
    departure_airport = serializers.SerializerMethodField()
    arrival_airport = serializers.SerializerMethodField()
    departure_time = serializers.SerializerMethodField()

    def get_departure_airport(self, obj):
        return obj.flight.departure_airport.name
    def get_arrival_airport(self, obj):
        return obj.flight.arrival_airport.name
    def get_departure_time(self, obj):
        return obj.flight.departure_time.strftime("%Y-%m-%d %H:%M")

    # arrival_airport = Flight.objects.filter(flight_number=flight).values('arrival_airport')
    # departure_time = Flight.objects.filter(flight_number=flight).values('departure_time')

    

    class Meta:
        model = Order
        fields = '__all__'
