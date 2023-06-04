from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegisterView,
    UserLoginView,
    UserDetailView,
    UserLogoutView,
    BulkFlightUpload,
    FlightAdminViewSet,
    FlightViewSet,
    CheckInView,
    TicketRefundView,
    TicketPurchaseView,
    AirportCreateAPIView,
    HomeView,
    get_city,
    get_airport,
    OrderViewSet,
    PassengerViewSet,
    TicketViewSet,
    CheckInRequestView,
    SendEmailView,
    UserChangeView,
    UserRetrieveView,
    CheckEmailView
)

app_name = 'core'
router = DefaultRouter()
router.register(r'flightadmin', FlightAdminViewSet, basename='flightadmin')
router.register(r'ticket', TicketViewSet, basename='ticket')
urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('userdetail/', UserDetailView.as_view(), name='userdetail'),
    path('ticketpurchase/', TicketPurchaseView.as_view(), name='ticketpurchase'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('bulkupload/',BulkFlightUpload.as_view(),name='bulkupload'),
    path('flight/',FlightViewSet.as_view(),name='flight'),
    path('order/',OrderViewSet.as_view(),name='order'),
    path('passenger/',PassengerViewSet.as_view(),name='passenger'),
    path('checkin/',CheckInView.as_view(),name="checkin"),
    path('checkinrequest/',CheckInRequestView.as_view(),name="checkinrequest"),
    path('refund/',TicketRefundView.as_view(),name="refund"),
    path('airport/create/',AirportCreateAPIView.as_view(),name="airport_create"),
    path('getcity/',get_city,name="getcity"),
    path('getairport/',get_airport,name="getairport"),
    path('sendemail/',SendEmailView.as_view(),name="sendemail"),
    path('retrieve/',UserRetrieveView.as_view(),name="retrieve"),
    path('userchange/',UserChangeView.as_view(),name="userchange"),
    path('checkemail/',CheckEmailView.as_view(),name="checkemail"),
] + router.urls
