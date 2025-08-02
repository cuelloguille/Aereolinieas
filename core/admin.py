from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Usuario, Avion, Vuelo, Pasajero, Asiento, Reserva, Boleto
from django.contrib.auth.admin import UserAdmin

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Rol', {'fields': ('rol',)}),
    )

admin.site.register(Avion)
admin.site.register(Vuelo)
admin.site.register(Pasajero)
admin.site.register(Asiento)
admin.site.register(Reserva)
admin.site.register(Boleto)
