# core/serializers.py
from rest_framework import serializers
from .models import Vuelo, Pasajero, Reserva, Avion, Boleto

class VueloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vuelo
        fields = '__all__'

class PasajeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pasajero
        fields = '__all__'

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'

class AvionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avion
        fields = '__all__'

class BoletoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boleto
        fields = '__all__'
