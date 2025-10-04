# core/api.py

from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Vuelo, Pasajero, Reserva, Avion, Boleto
from .serializers import VueloSerializer, PasajeroSerializer, ReservaSerializer, AvionSerializer, BoletoSerializer

# ---------------------------
# VUELOS
# ---------------------------
class VueloViewSet(viewsets.ModelViewSet):
    queryset = Vuelo.objects.all()
    serializer_class = VueloSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['origen', 'destino']
    ordering_fields = ['fecha', 'hora_salida']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    # Reporte: pasajeros por vuelo
    @action(detail=True, methods=['get'])
    def pasajeros(self, request, pk=None):
        vuelo = self.get_object()
        pasajeros = vuelo.reservas.filter(estado='confirmada').values('pasajero__id', 'pasajero__nombre', 'pasajero__email')
        return Response(pasajeros)

# ---------------------------
# PASAJEROS
# ---------------------------
class PasajeroViewSet(viewsets.ModelViewSet):
    queryset = Pasajero.objects.all()
    serializer_class = PasajeroSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.AllowAny()]  # cualquier usuario puede registrarse
        return [permissions.IsAuthenticated()]

    # Listar reservas de un pasajero
    @action(detail=True, methods=['get'])
    def reservas(self, request, pk=None):
        pasajero = self.get_object()
        reservas = pasajero.reservas.values('id', 'vuelo__origen', 'vuelo__destino', 'estado')
        return Response(reservas)

# ---------------------------
# RESERVAS
# ---------------------------
class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    # Cambiar estado de reserva
    @action(detail=True, methods=['post'])
    def cambiar_estado(self, request, pk=None):
        reserva = self.get_object()
        nuevo_estado = request.data.get('estado')
        if nuevo_estado not in ['confirmada', 'cancelada']:
            return Response({'error': 'Estado inválido'}, status=400)
        reserva.estado = nuevo_estado
        reserva.save()
        return Response({'status': 'ok', 'nuevo_estado': reserva.estado})

# ---------------------------
# AVIONES
# ---------------------------
class AvionViewSet(viewsets.ModelViewSet):
    queryset = Avion.objects.all()
    serializer_class = AvionSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    # Layout de asientos
    @action(detail=True, methods=['get'])
    def asientos(self, request, pk=None):
        avion = self.get_object()
        return Response({'asientos': avion.asientos_disponibles()})  # Método que deberías tener en tu modelo

# ---------------------------
# BOLETOS
# ---------------------------
class BoletoViewSet(viewsets.ModelViewSet):
    queryset = Boleto.objects.all()
    serializer_class = BoletoSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'list']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    # Generar boleto desde reserva confirmada
    @action(detail=False, methods=['post'])
    def generar(self, request):
        reserva_id = request.data.get('reserva_id')
        try:
            reserva = Reserva.objects.get(id=reserva_id, estado='confirmada')
        except Reserva.DoesNotExist:
            return Response({'error': 'Reserva no encontrada o no confirmada'}, status=404)
        
        boleto = Boleto.objects.create(reserva=reserva, codigo=f'B-{reserva.id:06d}')
        return Response({'status': 'ok', 'boleto_id': boleto.id, 'codigo': boleto.codigo})
