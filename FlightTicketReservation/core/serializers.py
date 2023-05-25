from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Flight, Ticket, Airport, Seat

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
        fields = ('username', 'password', 'email', 'credits')

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ['name','city','country']


class FlightSerializer(serializers.ModelSerializer):
    departure_airport = serializers.CharField()
    arrival_airport = serializers.CharField()
    economy_seats_available = serializers.SerializerMethodField()
    business_seats_available = serializers.SerializerMethodField()
    first_class_seats_available = serializers.SerializerMethodField()

    class Meta:
        model = Flight
        fields = '__all__'
        extra_kwargs = {
            'seats_remaining':{'required': False},
        }
    
    def get_economy_seats_available(self, obj):
        return Seat.objects.filter(flight=obj, type='3').filter(is_booked=False).count()

    def get_business_seats_available(self, obj):
        return Seat.objects.filter(flight=obj, type='2').filter(is_booked=False).count()

    def get_first_class_seats_available(self, obj):
        return Seat.objects.filter(flight=obj, type='1').filter(is_booked=False).count()
    
    def validate_departure_airport(self, value):
        try:
            Airport.objects.get(name=value)
        except Airport.DoesNotExist:
            raise serializers.ValidationError("Airport with this name does not exist.")
        return value

    def validate_arrival_airport(self, value):
        try:
            Airport.objects.get(name=value)
        except Airport.DoesNotExist:
            raise serializers.ValidationError("Airport with this name does not exist.")
        return value

    def create(self, validated_data):
        departure_airport_name = validated_data.pop('departure_airport')
        arrival_airport_name = validated_data.pop('arrival_airport')

        departure_airport = Airport.objects.get(name=departure_airport_name)
        arrival_airport = Airport.objects.get(name=arrival_airport_name)

        return Flight.objects.create(departure_airport=departure_airport, arrival_airport=arrival_airport, **validated_data)

    def update(self, instance, validated_data):
        departure_airport_name = validated_data.pop('departure_airport', None)
        arrival_airport_name = validated_data.pop('arrival_airport', None)

        if departure_airport_name is not None:
            instance.departure_airport = Airport.objects.get(name=departure_airport_name)
        if arrival_airport_name is not None:
            instance.arrival_airport = Airport.objects.get(name=arrival_airport_name)
        
        return super().update(instance, validated_data)



class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'