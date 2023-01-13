from django.db import models
from django.contrib.auth.models import User

class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    operation_airlines = models.CharField(max_length=15)
    departure_city = models.CharField(max_length=30)
    arrival_city = models.CharField(max_length=30)
    date_of_departure = models.DateField()
    etd = models.TimeField()
    
    def __str__(self):
        return f'{self.flight_number} - {self.departure_city} - {self.arrival_city}'


class Passenger(models.Model):   
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    phone_number = models.IntegerField()
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
# ! Relations'ları yazarken field ile Model name'i karşılaştırıyoruz
#  user-Reservation --> One-To-Many (ForeignKey)
#  passenger-Reservation --> Many-To-Many
#  flight-Reservation --> One-To-Many (ForeignKey)
class Reservation(models.Model):   
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # bir kullanıcı birden fazla rezervasyon yapabilir (ForeignKey)
    # ForeignKey (One-to-Many ilişki anlamına geliyor)
    passenger = models.ManyToManyField(Passenger, related_name="reservationPassenger")
    # ManyToMany relation tipinde on_delete belirtilmez.
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="reservationFlight")

    # * related_name'i anlamak için resimdeki tabloyu incele
    # Reservation modelinden flight field'ına direk ulaşabiliyorum
    # Fakat Flight modelinden Reservation modeline direkt iletişim yok bunun için related_name keyword'ü kullanılır.
    # yani related_name,child'tan parent'a iletişimde kullanılır
    def __str__(self):
        return f'{self.flight}/{self.user}'
    
    


   

    
    