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
    HomeView
)

app_name = 'core'
router = DefaultRouter()
router.register(r'flightadmin', FlightAdminViewSet, basename='flightadmin')
urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('userdetail/', UserDetailView.as_view(), name='userdetail'),
    path('ticketpurchase/', TicketPurchaseView.as_view(), name='ticketpurchase'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('bulkupload/',BulkFlightUpload.as_view(),name='bulkupload'),
    path('flight/',FlightViewSet.as_view(),name='flight'),
    path('checkin/',CheckInView.as_view(),name="checkin"),
    path('refund/',TicketRefundView.as_view(),name="refund"),
    path('airport/create/',AirportCreateAPIView.as_view(),name="airport_create"),
] + router.urls
