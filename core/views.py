# ========================
# IMPORTS
# ========================
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout

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
    width, height = letter

    # ===============================
    # Colores
    # ===============================
    color_header = (0.2, 0.4, 0.6)   # azul oscuro
    color_box = (0.95, 0.95, 0.95)   # gris claro
    color_code = (0.9, 0.2, 0.2)     # rojo para el código
    margin = 50

    # ===============================
    # Cabecera
    # ===============================
    p.setFillColorRGB(*color_header)
    p.rect(0, height - 100, width, 100, fill=True, stroke=False)
    p.setFillColorRGB(1, 1, 1)
    p.setFont("Helvetica-Bold", 24)
    p.drawCentredString(width / 2, height - 60, "Boleto de Reserva")

    # ===============================
    # Información del pasajero
    # ===============================
   

    p.setFillColorRGB(0, 0, 0)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(margin + 10, height - 150, "Pasajero:")
    p.setFont("Helvetica", 12)
    p.drawString(margin + 20, height - 170, f"Nombre: {reserva.pasajero.nombre}")
    p.drawString(margin + 20, height - 190, f"Documento: {reserva.pasajero.documento}")

    # ===============================
    # Información del vuelo
    # ===============================


    p.setFillColorRGB(0, 0, 0)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(margin + 10, height - 280, "Vuelo:")
    p.setFont("Helvetica", 12)
    p.drawString(margin + 20, height - 300, f"Ruta: {reserva.vuelo.origen} → {reserva.vuelo.destino}")
    p.drawString(margin + 20, height - 320, f"Fecha: {reserva.vuelo.fecha_salida.strftime('%d/%m/%Y %H:%M')}")
    p.drawString(margin + 20, height - 340, f"Asiento: {reserva.asiento.numero}")
    p.drawString(margin + 20, height - 360, f"Precio: ${reserva.precio:,.2f}")

    # ===============================
    # Código de reserva destacado
    # ===============================
    code_box_width = 250
    code_box_height = 60
    code_x = (width - code_box_width) / 2
    code_y = height - 450 - code_box_height

    p.setFillColorRGB(*color_code)
    p.roundRect(code_x, code_y, code_box_width, code_box_height, 8, fill=True, stroke=False)
    p.setFillColorRGB(1, 1, 1)
    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(width / 2, code_y + 20, reserva.codigo_reserva.upper())

    # Mensaje de privacidad sobre el código
    p.setFont("Helvetica-Oblique", 10)
    p.setFillColorRGB(0, 0, 0)
    p.drawCentredString(width / 2, code_y - 15, "Código de uso personal. No compartir con nadie.")

    # ===============================
    # Footer
    # ===============================
    p.setFont("Helvetica-Oblique", 10)
    p.setFillColorRGB(0.4, 0.4, 0.4)
    p.drawCentredString(width / 2, 30, "Gracias por elegir nuestra Aerolínea. ¡Buen viaje!")

    p.showPage()
    p.save()
    buffer.seek(0)

    return HttpResponse(buffer, content_type='application/pdf')
