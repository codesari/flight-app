from django.shortcuts import render
from rest_framework import viewsets
from .models import Flight,Reservation
from .serializers import FlightSerializer,ReservationSerializer,StaffFlightSerializer
# from rest_framework.permissions import  IsAdminUser
from .permissions import IsStafforReadOnly
from datetime import datetime, date


# Create your views here.
class FlightView(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    # permission_classes=[IsAdminUser]
    # permission_classes=(IsAdminUser,)
    permission_classes=[IsStafforReadOnly]

    # ! serializer_class metodunu override ediyoruz alttaki queryset gibi.çünkü uçuş için 2 tane serializer yazdık,duruma göre onları tercih ettireceğiz.

    def get_serializer_class(self):
        serializer=super().get_serializer_class()
        # parent'taki serializer'ı al
        if self.request.user.is_staff:
            return StaffFlightSerializer
        return serializer
    
    # ? staff olmayan kullanıcı geçmiş flight'ları görmesin.
    def get_queryset(self):
        now = datetime.now()
        current_time = now.strftime('%H:%M:%S')
        today = date.today()
        
        if self.request.user.is_staff:
            return super().get_queryset()
        
        else:
             # ? ve bugün ve bugünden sonraki tarihleri göster
            queryset = Flight.objects.filter(date_of_departure__gt=today)
                # ? bugünkü flight'lar için saat kontrolü
            if Flight.objects.filter(date_of_departure=today):
                today_qs = Flight.objects.filter(date_of_departure=today).filter(etd__gt=current_time)

                queryset = queryset.union(today_qs)
            return queryset



class ReservationsView(viewsets.ModelViewSet):
     queryset = Reservation.objects.all()
     serializer_class = ReservationSerializer
    
    # ! queryset metodunu override yaparak filtreleme yapıyoruz
     def get_queryset(self):
        queryset = super().get_queryset()
        # parent'daki queryset'i getirir
        # queryset = Reservation.objects.all() yazsakta olurdu fakat dinamik olması için yukarıdaki gibi yazdık
        if self.request.user.is_staff:
            # views ortamında request.user diyerek istek atan user'a direk erişebiliyorum.serializers'da farklı bir yapı vardı (context)
            return queryset
        return queryset.filter(user= self.request.user)

        # ! if blogu özet :
        # eğer istek atan admin ise tüm userlara ait rezervasyonları döndür
        # değilse istek atan user'ın sadece kendi rezervasyonlarını listele