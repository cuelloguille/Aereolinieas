# ========================
# IMPORTS
# ========================
from collections import defaultdict
import random
import string
import io

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db import transaction, IntegrityError
from django.http import HttpResponse

from .models import Vuelo, Pasajero, Reserva, Asiento
from .forms import RegistroForm

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# ========================
# LOGIN PERSONALIZADO
# ========================
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirección según rol
            if user.is_staff or user.is_superuser:
                messages.success(request, f"Bienvenido, Admin {user.username}!")
                return redirect('/admin/')
            else:
                messages.success(request, f"Bienvenido, {user.username}!")
                return redirect('vuelos_list')
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})


# ========================
# LISTADO DE VUELOS CON FILTROS
# ========================
@login_required
def vuelos_list(request):
    vuelos = Vuelo.objects.filter(estado='activo')

    # Parámetros de búsqueda
    origen = request.GET.get('origen', '').strip()
    destino = request.GET.get('destino', '').strip()
    fecha = request.GET.get('fecha', '').strip()  # formato 'YYYY-MM-DD'

    # Aplicar filtros
    if origen:
        vuelos = vuelos.filter(origen__icontains=origen)
    if destino:
        vuelos = vuelos.filter(destino__icontains=destino)
    if fecha:
        vuelos = vuelos.filter(fecha_salida__date=fecha)

    context = {
        'vuelos': vuelos,
        'origen': origen,
        'destino': destino,
        'fecha': fecha,
    }
    return render(request, 'core/vuelos_list.html', context)


# ========================
# RESERVA DE VUELOS
# ========================
@login_required
def reservar_vuelo(request, vuelo_id):
    vuelo = get_object_or_404(Vuelo, id=vuelo_id, estado='activo')

    try:
        pasajero = request.user.pasajero
    except Pasajero.DoesNotExist:
        messages.error(request, "Debes completar tu perfil antes de reservar.")
        return redirect('perfil_pasajero')

    asientos_del_avion = vuelo.avion.asientos.all()
    asientos_ocupados = Reserva.objects.filter(vuelo=vuelo, estado='activa').values_list('asiento_id', flat=True)
    asientos_disponibles = asientos_del_avion.exclude(id__in=asientos_ocupados)

    # Agrupar asientos por fila
    asientos_por_fila = defaultdict(list)
    for asiento in asientos_del_avion.order_by('fila', 'columna'):
        asientos_por_fila[asiento.fila].append(asiento)

    if request.method == 'POST':
        asiento_id = request.POST.get('asiento_id')
        if not asiento_id:
            messages.error(request, "Debes seleccionar un asiento.")
            return redirect('reservar_vuelo', vuelo_id=vuelo.id)

        asiento = get_object_or_404(Asiento, id=asiento_id, avion=vuelo.avion)

        if Reserva.objects.filter(vuelo=vuelo, asiento=asiento, estado='activa').exists():
            messages.error(request, "El asiento ya está reservado.")
            return redirect('reservar_vuelo', vuelo_id=vuelo.id)

        try:
            with transaction.atomic():
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
                messages.success(request, f"Reserva creada con éxito. Código: {codigo}")
                return redirect('mis_reservas')
        except IntegrityError:
            messages.error(request, "Ocurrió un error. Intenta nuevamente.")

    return render(request, 'core/reservar_vuelo.html', {
        'vuelo': vuelo,
        'asientos_disponibles': asientos_disponibles,
        'asientos_por_fila': asientos_por_fila,
    })


# ========================
# MIS RESERVAS
# ========================
@login_required
def mis_reservas(request):
    try:
        pasajero = request.user.pasajero
    except Pasajero.DoesNotExist:
        messages.error(request, "Debes completar tu perfil para ver tus reservas.")
        return redirect('perfil_pasajero')

    reservas = Reserva.objects.filter(pasajero=pasajero, estado='activa').select_related('vuelo', 'asiento')
    return render(request, 'core/mis_reservas.html', {'reservas': reservas})


# ========================
# CANCELAR RESERVA
# ========================
@login_required
def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, pasajero__usuario=request.user, estado='activa')

    if request.method == 'POST':
        with transaction.atomic():
            reserva.estado = 'cancelada'
            if reserva.asiento:
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
            documento = form.cleaned_data.get('documento')
            if Pasajero.objects.filter(documento=documento).exists():
                messages.error(request, "El documento ya está registrado.")
                return redirect('registro')

            try:
                with transaction.atomic():
                    user = form.save(commit=False)
                    user.rol = 'cliente'
                    user.save()
                    Pasajero.objects.create(
                        usuario=user,
                        nombre=form.cleaned_data.get('nombre'),
                        documento=documento,
                        email=form.cleaned_data.get('email'),
                        telefono=form.cleaned_data.get('telefono'),
                        fecha_nacimiento=form.cleaned_data.get('fecha_nacimiento'),
                        tipo_documento=form.cleaned_data.get('tipo_documento'),
                    )
                login(request, user)
                messages.success(request, f"Registro exitoso. ¡Bienvenido, {user.username}!")
                return redirect('vuelos_list')
            except IntegrityError:
                messages.error(request, "Ocurrió un error al registrar el usuario. Intenta de nuevo.")
                return redirect('registro')
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = RegistroForm()
    return render(request, 'core/registro.html', {'form': form})


# ========================
# GENERAR BOLETO PDF
# ========================
@login_required
def generar_boleto_pdf(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, pasajero__usuario=request.user)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Cabecera
    p.setFillColorRGB(0.2, 0.4, 0.6)
    p.rect(0, height - 100, width, 100, fill=True, stroke=False)
    p.setFillColorRGB(1, 1, 1)
    p.setFont("Helvetica-Bold", 24)
    p.drawCentredString(width / 2, height - 60, "Boleto de Reserva")

    # Pasajero y vuelo
    p.setFillColorRGB(0, 0, 0)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 150, "Pasajero:")
    p.setFont("Helvetica", 12)
    p.drawString(60, height - 170, f"Nombre: {reserva.pasajero.nombre}")
    p.drawString(60, height - 190, f"Documento: {reserva.pasajero.documento}")
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 280, "Vuelo:")
    p.setFont("Helvetica", 12)
    fecha_vuelo = reserva.vuelo.fecha_salida.strftime('%d/%m/%Y %H:%M') if hasattr(reserva.vuelo, 'fecha_salida') else "Fecha no disponible"
    asiento_numero = reserva.asiento.numero if reserva.asiento else "Sin asignar"
    p.drawString(60, height - 300, f"Ruta: {reserva.vuelo.origen} → {reserva.vuelo.destino}")
    p.drawString(60, height - 320, f"Fecha: {fecha_vuelo}")
    p.drawString(60, height - 340, f"Asiento: {asiento_numero}")
    p.drawString(60, height - 360, f"Precio: ${reserva.precio:,.2f}")

    # Código
    code_box_width = 250
    code_box_height = 60
    code_x = (width - code_box_width) / 2
    code_y = height - 450 - code_box_height
    p.setFillColorRGB(0.9, 0.2, 0.2)
    p.roundRect(code_x, code_y, code_box_width, code_box_height, 8, fill=True, stroke=False)
    p.setFillColorRGB(1, 1, 1)
    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(width / 2, code_y + 20, reserva.codigo_reserva.upper())

    # Footer
    p.setFont("Helvetica-Oblique", 10)
    p.setFillColorRGB(0.4, 0.4, 0.4)
    p.drawCentredString(width / 2, 30, "Gracias por elegir nuestra Aerolínea. ¡Buen viaje!")

    p.showPage()
    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')


# ========================
# DETALLE DE VUELO
# ========================
def detalle_vuelo(request, pk):
    vuelo = get_object_or_404(Vuelo, pk=pk)
    reservas = vuelo.reservas.all()
    asientos = vuelo.avion.asientos.all()
    return render(request, 'core/detalle_de_vuelo.html', {
        'vuelo': vuelo,
        'reservas': reservas,
        'asientos': asientos,
    })
