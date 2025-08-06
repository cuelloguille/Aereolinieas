# ========================
# IMPORTS
# ========================
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction, IntegrityError
from django.http import HttpResponse
import random
import string
import io

from .models import Vuelo, Pasajero, Reserva, Asiento
from .forms import RegistroForm

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


# ========================
# VISTAS DE VUELOS
# ========================

@login_required
def vuelos_list(request):
    vuelos = Vuelo.objects.filter(estado='activo')
    return render(request, 'core/vuelos_list.html', {'vuelos': vuelos})


# ========================
# VISTAS DE RESERVAS
# ========================

@login_required
def reservar_vuelo(request, vuelo_id):
    vuelo = get_object_or_404(Vuelo, id=vuelo_id, estado='activo')

    try:
        pasajero = request.user.pasajero
    except Pasajero.DoesNotExist:
        messages.error(request, "Debes completar tu perfil antes de reservar.")
        return redirect('perfil_pasajero')

    asientos_del_avion = Asiento.objects.filter(avion=vuelo.avion)
    asientos_ocupados = Reserva.objects.filter(vuelo=vuelo, estado='activa').values_list('asiento_id', flat=True)
    asientos_disponibles = asientos_del_avion.exclude(id__in=asientos_ocupados)

    if request.method == 'POST':
        asiento_id = request.POST.get('asiento_id')
        if not asiento_id:
            messages.error(request, "Debes seleccionar un asiento.")
            return redirect('reservar_vuelo', vuelo_id=vuelo.id)

        asiento = get_object_or_404(Asiento, id=asiento_id, avion=vuelo.avion)

        if Reserva.objects.filter(vuelo=vuelo, asiento=asiento, estado='activa').exists():
            messages.error(request, "El asiento seleccionado ya fue reservado.")
            return redirect('reservar_vuelo', vuelo_id=vuelo.id)

        if Reserva.objects.filter(vuelo=vuelo, pasajero=pasajero, estado='activa').exists():
            messages.error(request, "Ya tienes una reserva activa para este vuelo.")
            return redirect('mis_reservas')

        try:
            with transaction.atomic():
                asiento = Asiento.objects.select_for_update().get(id=asiento_id)

                if Reserva.objects.filter(vuelo=vuelo, asiento=asiento, estado='activa').exists():
                    messages.error(request, "Otro usuario reservó ese asiento justo ahora.")
                    return redirect('reservar_vuelo', vuelo_id=vuelo.id)

                codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

                Reserva.objects.create(
                    vuelo=vuelo,
                    pasajero=pasajero,
                    asiento=asiento,
                    estado='activa',
                    precio=vuelo.precio_base,
                    codigo_reserva=codigo,
                )

                asiento.estado = 'ocupado'
                asiento.save()

        except IntegrityError:
            messages.error(request, "Ese asiento ya fue reservado por otro usuario.")
            return redirect('reservar_vuelo', vuelo_id=vuelo.id)

        messages.success(request, f"Reserva creada con éxito. Código: {codigo}")
        return redirect('mis_reservas')

    return render(request, 'core/reservar_vuelo.html', {
        'vuelo': vuelo,
        'asientos_disponibles': asientos_disponibles,
    })


@login_required
def mis_reservas(request):
    try:
        pasajero = request.user.pasajero
    except Pasajero.DoesNotExist:
        messages.error(request, "Debes completar tu perfil para ver tus reservas.")
        return redirect('perfil_pasajero')

    reservas = Reserva.objects.filter(pasajero=pasajero, estado='activa').select_related('vuelo', 'asiento')
    return render(request, 'core/mis_reservas.html', {'reservas': reservas})


@login_required
def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, pasajero__usuario=request.user, estado='activa')

    if request.method == 'POST':
        with transaction.atomic():
            reserva.estado = 'cancelada'
            reserva.asiento.estado = 'disponible'
            reserva.asiento.save()
            reserva.save()

        messages.success(request, "Reserva cancelada correctamente.")
        return redirect('mis_reservas')

    return render(request, 'core/cancelar_reserva.html', {'reserva': reserva})


# ========================
# REGISTRO DE USUARIOS
# ========================

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registro exitoso. ¡Bienvenido/a!")
            return redirect('vuelos_list')
        else:
            messages.error(request, "Error en el registro.")
    else:
        form = RegistroForm()

    return render(request, 'core/registro.html', {'form': form})


# ========================
# GENERAR BOLETO EN PDF
# ========================

@login_required
def generar_boleto_pdf(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, pasajero__usuario=request.user)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # Cabecera
    p.setFont("Helvetica-Bold", 18)
    p.drawString(180, 750, "Boleto de Reserva")

    # Detalles
    p.setFont("Helvetica", 12)
    p.drawString(100, 700, f"Pasajero: {reserva.pasajero.nombre}")
    p.drawString(100, 680, f"Documento: {reserva.pasajero.documento}")
    p.drawString(100, 660, f"Vuelo: {reserva.vuelo.origen} → {reserva.vuelo.destino}")
    p.drawString(100, 640, f"Fecha de salida: {reserva.vuelo.fecha_salida.strftime('%d/%m/%Y %H:%M')}")
    p.drawString(100, 620, f"Asiento: {reserva.asiento.numero}")
    p.drawString(100, 600, f"Código de Reserva: {reserva.codigo_reserva}")
    p.drawString(100, 580, f"Precio: ${reserva.precio}")

    p.showPage()
    p.save()
    buffer.seek(0)

    return HttpResponse(buffer, content_type='application/pdf')
