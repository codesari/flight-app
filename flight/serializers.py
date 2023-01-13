from rest_framework import serializers
from .models import Flight,Reservation,Passenger

class FlightSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Flight
        fields = (
            "id",
            "flight_number",
            "operation_airlines",
            "departure_city",
            "arrival_city",
            "date_of_departure",
            "etd"
        )

class PassengerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Passenger
        fields="__all__"

class ReservationSerializer(serializers.ModelSerializer):

    
    passenger=PassengerSerializer(many=True)
    flight=serializers.StringRelatedField()
    # StringRelatedField --> __str__ fonksiyonundaki ismi gelsin
    flight_id=serializers.IntegerField()
    # create ederken sadece flight ile ekleyemiyorum bu yüzden flight_id'yi de ekledim
    user=serializers.StringRelatedField()
    class Meta:
        model=Reservation
        # fields="__all__"
        fields=("id","flight","flight_id","user","passenger")

    def create(self, validated_data):
        passenger_data = validated_data.pop("passenger")
        # gelen data'dan passenger datasını çıkarttım
        validated_data["user_id"] = self.context["request"].user.id
        # gelen veriye user_id'yi eklemem için user_id'ye ulaşma kodu
        reservationFlight = Reservation.objects.create(**validated_data)
        
        # her bir passenger datasını passenger tablosuna kaydettim
        for passenger in passenger_data:
            pas = Passenger.objects.create(**passenger)
            reservationFlight.passenger.add(pas)
            # many-to-many'de fieldları bu şekilde ekliyoruz
        
        reservationFlight.save()
        return reservationFlight

# Staff'a özel bir FlightSerializer yazıyorum

class StaffFlightSerializer(serializers.ModelSerializer):
    
    reservationFlight=ReservationSerializer(many=True,read_only=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "flight_number",
            "operation_airlines",
            "departure_city",
            "arrival_city",
            "date_of_departure",
            "etd",
            "reservationFlight"
        )

# ! Uçuşları listeleyen 2 tane serializers'ım var.FlightSerializer ve StaffFlightSerializer.StaffFlightSerializer daha detaylısı içinde passaengerlar da var