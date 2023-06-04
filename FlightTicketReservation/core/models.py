from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import *  
# Create your models here.

Credit_choices = (
    ('1', 'good'),
    ('2', 'bad'),
)

Flight_choices = (
    ('1', 'available'),
    ('2', 'full'),
    ('3', 'cancelled'),
    ('4', 'delayed'),
)

Ticket_choices = (
    ('1', 'purchased'),
    ('2', 'pending check-in'),
    ('2', 'checked in'),
    ('3', 'cancelled'),
)
Seat_choices = (
    ('1','First Class'),
    ('2','Business Class'),
    ('3','Economy Class'),
)


class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    credits = models.IntegerField(default=100)
    travel_num = models.IntegerField(default=0)
    user_nickname = models.CharField(max_length=200, default=None)
    last_recover_date = models.DateField(null=True,blank=True)

class Passenger(models.Model):
    id_card_number = models.CharField(max_length=18, unique=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)

    # any other fields...

    def __str__(self):
        return self.full_name


class Airport(models.Model):
    IATA_code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=200, unique=True)
    city = models.CharField(max_length=200)
    city_name = models.CharField(max_length=200, default=None)
    country = models.CharField(max_length=200)

    def get_city():
        city_list = []

        airports = Airport.objects.values('city','city_name').distinct()
        for airport in airports:
            city_list.append({'value':airport['city'],'label':airport['city_name']})
        return city_list
    


    

    def __str__(self):
        return self.name + ' ' + self.city + ' ' + self.country

class Flight(models.Model):
    flight_number = models.CharField(max_length=200, unique=True)
    departure_city = models.CharField(max_length=200)
    departure_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departure_airport')
    arrival_city = models.CharField(max_length=200)
    arrival_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrival_airport')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField(default=0)
    status = models.CharField(max_length=200,choices=Flight_choices, default='1')
    seats_remaining = models.IntegerField(default=None)
    insurance = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.seats_remaining is None:
            self.seats_remaining = self.capacity
        super().save(*args, **kwargs) 

    def __str__(self):
        return self.flight_number
    
class Ticket(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, default=None)
    seat = models.IntegerField(default=1)
    status = models.CharField(max_length=200,choices=Ticket_choices, default='1')
    date_of_purchase = models.DateTimeField(auto_now_add=True)
    food_option = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)

    def __str__(self):
        return self.flight.flight_number + ' ' + self.passenger.full_name + ' ' + self.seat

class Order(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tickets = models.ManyToManyField(Ticket)

    def __str__(self):
        return self.flight.flight_number + ' ' + self.customer.username

    
class Seat(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seatnum = models.IntegerField(default=1)
    type = models.CharField(choices=Seat_choices, max_length=200, default='1')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_booked = models.BooleanField(default=False)

    # class Meta:
    #     unique_together = ['flight', 'seatnum']

    def is_available(self):
        return not self.is_booked

    def __str__(self):
        return self.flight.flight_number + ' ' + self.seatnum
      

    
@receiver(post_save, sender=Flight)
def post_save_receiver(sender, instance, created, *args, **kwargs):
    if created:
        for i in range(1, instance.capacity + 1):
            if i <= int(instance.capacity * Decimal(0.1)):
                Seat.objects.create(flight=instance, seatnum=i, type='1', price = instance.price*Decimal(1.5))
            elif i <= int(instance.capacity * Decimal(0.2)):
                Seat.objects.create(flight=instance, seatnum=i, type='2', price = instance.price*Decimal(1.2))
            else:
                Seat.objects.create(flight=instance, seatnum=i, type='3', price = instance.price)





