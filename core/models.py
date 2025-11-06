from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# ---------------------------
# Usuario extendido para agregar rol
# ---------------------------
class Usuario(AbstractUser):
    ROL_CHOICES = (
        ('admin', 'Administrador'),
        ('gestor', 'Gestor de vuelos'),
        ('cliente', 'Cliente / Pasajero'),
    )
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='cliente')

    # Evitar conflictos con auth.User
    groups = models.ManyToManyField(
        Group,
        related_name='core_usuarios',  # nombre único para este modelo
        blank=True,
        help_text='Los grupos a los que pertenece este usuario.',
        verbose_name='grupos',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='core_usuarios_permissions',  # nombre único para este modelo
        blank=True,
        help_text='Permisos específicos para este usuario.',
        verbose_name='permisos de usuario',
    )

    def __str__(self):
        return self.username


# ---------------------------
# Avión y Asientos
# ---------------------------
class Avion(models.Model):
    modelo = models.CharField(max_length=100)
    capacidad = models.PositiveIntegerField()
    filas = models.PositiveIntegerField()
    columnas = models.PositiveIntegerField()

    def __str__(self):
        return self.modelo

class Asiento(models.Model):
    ESTADO_CHOICES = (
        ('disponible', 'Disponible'),
        ('reservado', 'Reservado'),
        ('ocupado', 'Ocupado'),
    )

    avion = models.ForeignKey(Avion, on_delete=models.CASCADE, related_name='asientos')
    numero = models.CharField(max_length=10)
    fila = models.PositiveIntegerField()
    columna = models.CharField(max_length=1)
    tipo = models.CharField(max_length=20, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='disponible')

    class Meta:
        unique_together = ('avion', 'numero')

    def __str__(self):
        return f"{self.numero} ({self.estado})"


# ---------------------------
# Vuelos
# ---------------------------
class Vuelo(models.Model):
    avion = models.ForeignKey(Avion, on_delete=models.PROTECT, related_name='vuelos')
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    fecha_salida = models.DateTimeField()
    fecha_llegada = models.DateTimeField()
    duracion = models.DurationField()
    estado = models.CharField(max_length=20, default='activo')
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    gestores = models.ManyToManyField(
        Usuario,
        related_name='vuelos_gestionados',
        limit_choices_to={'rol': 'gestor'},
        blank=True
    )

    def __str__(self):
        return f"{self.origen} -> {self.destino} ({self.fecha_salida.strftime('%Y-%m-%d %H:%M')})"


# ---------------------------
# Pasajeros
# ---------------------------
class Pasajero(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='pasajero')
    nombre = models.CharField(max_length=100)
    documento = models.CharField(max_length=30, unique=True)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    tipo_documento = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


# ---------------------------
# Reservas
# ---------------------------
class Reserva(models.Model):
    ESTADO_CHOICES = (
        ('activa', 'Activa'),
        ('cancelada', 'Cancelada'),
        ('finalizada', 'Finalizada'),
    )

    vuelo = models.ForeignKey(Vuelo, on_delete=models.CASCADE, related_name='reservas')
    pasajero = models.ForeignKey(Pasajero, on_delete=models.CASCADE, related_name='reservas')
    asiento = models.ForeignKey(Asiento, on_delete=models.PROTECT, related_name='reservas')
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activa')
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    codigo_reserva = models.CharField(max_length=12, unique=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['vuelo', 'asiento'], name='reserva_asiento_unico_por_vuelo'),
            models.UniqueConstraint(fields=['vuelo', 'pasajero'], name='reserva_pasajero_unico_por_vuelo'),
        ]

    def __str__(self):
        return f"{self.codigo_reserva} - {self.pasajero} en {self.vuelo}"


# ---------------------------
# Boletos
# ---------------------------
class Boleto(models.Model):
    ESTADO_CHOICES = (
        ('emitido', 'Emitido'),
        ('usado', 'Usado'),
        ('cancelado', 'Cancelado'),
    )

    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE, related_name='boleto')
    codigo_barra = models.CharField(max_length=50, unique=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='emitido')

    def __str__(self):
        return f"Boleto {self.codigo_barra} para {self.reserva.codigo_reserva}"



from django.utils import timezone
from django.conf import settings

# ---------------------------
# Mensajes / Solicitudes (Cambio de asiento, cancelación, consulta)
# ---------------------------
class Mensaje(models.Model):
    TIPO_SOLICITUD_CHOICES = (
        ('cambio_asiento', 'Cambio de asiento'),
        ('cancelacion', 'Cancelación de vuelo'),
        ('consulta', 'Consulta general'),
    )

    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('respondido', 'Respondido'),
        ('cerrado', 'Cerrado'),
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mensajes_enviados'
    )
    vuelo = models.ForeignKey('Vuelo', on_delete=models.CASCADE, related_name='mensajes')
    reserva = models.ForeignKey('Reserva', on_delete=models.CASCADE, related_name='mensajes')
    asiento_solicitado = models.ForeignKey(
        'Asiento',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='mensajes'
    )

    tipo_solicitud = models.CharField(max_length=30, choices=TIPO_SOLICITUD_CHOICES)
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(default=timezone.now)

    respuesta_admin = models.TextField(blank=True, null=True)
    fecha_respuesta = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    def __str__(self):
        return f"Solicitud de {self.usuario.username} - {self.get_tipo_solicitud_display()}"

from django.db import models
from django.conf import settings
from django.utils import timezone

class Mensaje(models.Model):
    TIPO_SOLICITUD_CHOICES = (
        ('cambio_asiento', 'Cambio de asiento'),
        ('cancelacion', 'Cancelación de vuelo'),
        ('consulta', 'Consulta general'),
    )

    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('respondido', 'Respondido'),
        ('cerrado', 'Cerrado'),
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mensajes_enviados'
    )
    vuelo = models.ForeignKey('Vuelo', on_delete=models.CASCADE, related_name='mensajes')
    reserva = models.ForeignKey('Reserva', on_delete=models.CASCADE, related_name='mensajes')
    asiento_solicitado = models.ForeignKey(
        'Asiento', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='mensajes'
    )

    tipo_solicitud = models.CharField(max_length=30, choices=TIPO_SOLICITUD_CHOICES)
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(default=timezone.now)

    respuesta_admin = models.TextField(blank=True, null=True)
    fecha_respuesta = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    def __str__(self):
        return f"Solicitud de {self.usuario.username} - {self.get_tipo_solicitud_display()}"
